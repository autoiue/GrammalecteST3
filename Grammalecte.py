import sublime
import sublime_plugin
import subprocess
import tempfile
import json
import os
import time

# stores the plugin states for the different views
view_states = {}

# TODO: manage this through a sublime-config file
ignore_ruleid = ['esp_fin_ligne']
autorun_interval_seconds = 2

# Get a state for a particular view
def get_state(view):
	global view_states

	# create if first time seen
	if view.id() not in view_states:
		view_states[view.id()] = {
			'errors' : [],
			'showing_gramma' : False,
			'show_apos' : False,
			'show_spaces' : False,
			'regions' : [],
			'next_auto_run' : 0
		}
	return view_states[view.id()]

# get the error underneath a set of 'dip' coordinates 
def event_to_error(event, view):
	pt = view.window_to_text((event["x"], event["y"]))
	return point_to_error(pt, view)

# get the error at a particular text point
def point_to_error(point, view):

	# get an actualised set of regions
	regions = view.get_regions("gramma")
	reg_index = 0

	# look through set to find the first region cointaing the text point
	for reg in regions:
		if reg.begin() <= point:
			if reg.end() >= point:
				# get the corresponding error
				# TODO : not rely on lists orders to find error 
				return get_state(view)['errors'][reg_index]
		reg_index += 1
	# if none found, return None
	return None


# Text command (re)executing Grammalecte on the current buffer content

class GrammaRunCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		runGrammalecte(self.view)

	def is_enabled(self):
		return True

	def description(self):
		if get_state(self.view)['showing_gramma']:
			return "Rerun Grammalecte"
		else:
			return "Run Grammalecte"
		pass

# save the current buffer to grammalecte-cli.py (must be in path), reflect results in view

def runGrammalecte(view):
	global ignore_ruleid, autorun_interval_seconds
	
	# get full buffer content and save it to a temp file (this is system independant)
	contents = view.substr(sublime.Region(0, view.size()-1))
	temp_file, filename = tempfile.mkstemp()
	os.write(temp_file, bytes(contents, 'UTF-8'))
	os.close(temp_file)

	# send temp file to cli (must be in path, not system indepentant, currently only tested on Linux system)
	# get and parse JSON result
	result = subprocess.check_output(['grammalecte-cli.py', '-f', filename, '-j'])
	gramma = json.loads(result.decode('utf-8'))

	# get plugin state for this view
	state = get_state(view)

	# check that Grammalecte landed results 
	if "data" in gramma:
		data = gramma['data']

		# reset state
		state['regions'] = []
		state['errors'] = []
		state['show_apos'] = False

		# go through result, paragraph by pragraph
		region_index = 0
		prev_end = 0
		for p in data:
			# get ordinate of line to offset Grammlacte ordinate that has an origin
			# at line start contrarly to Sublime that has origin at document start
			line_begin = view.text_point(p['iParagraph']-1, 0)

			# for each error, sorted by order of appearence :
			for grammar_error in sorted(p['lGrammarErrors'], key=lambda err: err['nStart']):
				#print("ERR:"+str(region_index)+"> " + grammar_error['sMessage'])

				# check that rule is not in ignore list
				if grammar_error['sRuleId'] not in ignore_ruleid:

					# if intersecting errors, ignore the last
					if line_begin+grammar_error['nStart'] >= prev_end:

						# flag the presence of common type errors
						if grammar_error['sRuleId'] == "apostrophe_typographique":
							state['show_apos'] = True
						if grammar_error['sType'] == "nbsp":
							state['show_spaces'] = True

						# create region for error that will be displayed in the view
						error_region = sublime.Region(line_begin+grammar_error['nStart'],line_begin+grammar_error['nEnd'])
						state['regions'].append(error_region)

						# store error along with view dependant data
						state['errors'].append({
									  "start":line_begin+grammar_error['nStart'],
									  "end":line_begin+grammar_error['nEnd'],
									  "region" : region_index,
									  "gdata":grammar_error
									  })
						# update index to keep track of which region correspond to which error
						region_index += 1

						# keep track of the minimum position for the next error to avoid intersecting errors
						prev_end = line_begin+grammar_error['nEnd']
				pass
			pass

		
		# draw error/regions on view
		view.add_regions("gramma", state['regions'], "entity", "dot", sublime.DRAW_NO_FILL | sublime.DRAW_SQUIGGLY_UNDERLINE | sublime.PERSISTENT)

		# flag to show that we up and running
		state['showing_gramma'] = True

		# set next autorun time
		state['next_auto_run'] = time.time() + autorun_interval_seconds

		# print that we are ready in the status bar
		view.window().status_message("Grammalecte : "+str(len(state['errors']))+" grammar error"+ ("s" if len(state['errors']) > 1 else "")+" found.")

	pass

# do a replacement of erroned text by suggested text
def replaceBySuggestion(view, edit, err):

	# check that at least one suggestion exist for the error
	if len(err['gdata']['aSuggestions']) > 0 :

		# get the updated region from the view
		# (regions could be shifted by previous user input)
		regions = view.get_regions("gramma")

		# get the region to remplace using index
		# (TODO, find another way of identifying and getting regions)
		region_to_replace = regions[err['region']]

		# do re replacement
		view.replace(edit, region_to_replace, err['gdata']['aSuggestions'][0])

		# get the plugin state for this view
		state = get_state(view)

		# remove the region and the error
		state['errors'].remove(err)
		regions.remove(region_to_replace)
		new_regions = []

		# check if len(old) != len(new)
		# if so, regions are not automatically updated
		# and need a bit of shifting
		diff = len(err['gdata']['aSuggestions'][0]) - region_to_replace.size()
		if diff is not 0:
			for r in regions:
				if region_to_replace.begin() < r.begin():
					new_regions.append(sublime.Region(r.begin() + diff, r.end() + diff))
				else:
					new_regions.append(r)
		else:
			new_regions = regions

		# update the indexes
		for e in state['errors']:
			if e['region'] > err['region']:
				e['region'] -= 1

		# redraw view
		view.add_regions("gramma", new_regions, "entity", "dot", sublime.DRAW_NO_FILL | sublime.DRAW_SQUIGGLY_UNDERLINE | sublime.PERSISTENT)
	pass

# command to shut down the plugin
class GrammaClearCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		# erase regions from view
		self.view.erase_regions("gramma")

		# flag that we not running anymore for this view
		get_state(view)['showing_gramma'] = False

	# display command in context menu only id we're running
	def is_visible(self):
		return get_state(self.view)['showing_gramma']

# command to bulk-resolve all typograhic apostrophes related arrors
class GrammaAposCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		# go through errors by the end to avoid most of the errors ordinates shifting
		errors_fixed = 0
		for err in reversed(get_state(self.view)['errors']):

			# solve only if errors correspond to a specific rule
			if err["gdata"]["sRuleId"] == "apostrophe_typographique":
				replaceBySuggestion(self.view, edit, err)
				errors_fixed += 1

		# Display how many errors we fixed
		self.view.window().status_message("Grammalecte fixed "+str(errors_fixed)+" error"+ ("s" if errors_fixed > 1 else "")+".")
				
		# set flag off
		get_state(self.view)['show_apos'] = False

	# only show if flag is set
	def is_visible(self):
		return get_state(self.view)['show_apos']

# command to bulk-resolve all unbreakable space related arrors
class GrammaSpacesCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		# go through errors by the end to avoid most of the errors ordinates shifting
		errors_fixed = 0
		for err in reversed(get_state(self.view)['errors']):

			# solve only if errors correspond to a set rule/type
			if err["gdata"]["sType"] == "nbsp" or err["gdata"]["sRuleId"] == "num_grand_nombre_avec_espaces":
				replaceBySuggestion(self.view, edit, err)
				errors_fixed += 1

		# Display how many errors we fixed
		self.view.window().status_message("Grammalecte fixed "+str(errors_fixed)+" error"+ ("s" if errors_fixed > 1 else "")+".")

		# set flag off
		get_state(self.view)['show_spaces'] = False

	# only show if flag is set
	def is_visible(self):
		return get_state(self.view)['show_spaces']

# command to bulk-resolve errors of the kind of the one under the mouse
class GrammaFixAllCurrentCommand(sublime_plugin.TextCommand):
	def run(self, edit, event):

		# get the error under the mouse
		error = event_to_error(event, self.view)

		# if any :
		if error is not None:

			# got through all errors, and resolve if ruleId correspond
			errors_fixed = 0
			for err in reversed(get_state(self.view)['errors']):
				if err["gdata"]["sRuleId"] == error['gdata']['sRuleId']:
					replaceBySuggestion(self.view, edit, err)
					errors_fixed += 1

			# Display how many errors we fixed
			self.view.window().status_message("Grammalecte fixed "+str(errors_fixed)+" error"+ ("s" if errors_fixed > 1 else "")+".")

	# only show if there is an error under the mouse
	# and there is at least on suggestion 
	def is_visible(self, event):
		error = event_to_error(event, self.view)
		if error is None: return False
		return len(error['gdata']['aSuggestions']) is not 0

	# we want to get mouse coordinates
	# when command executed
	def want_event(self):
		return True

# command to apply the first suggestion to solve an error
class GrammaSuggestCommand(sublime_plugin.TextCommand):

	def run(self, edit, event):

		# get the error under the mouse
		error = event_to_error(event, self.view)

		# if any, solve this error
		if error is not None:
			replaceBySuggestion(self.view, edit, error)
		pass

	# only show if there is an error under the mouse
	def is_visible(self, event):
		error = event_to_error(event, self.view)
		return error is not None

	# only show if there is an error under the mouse
	# and there is at least one suggestion
	def is_enabled(self, event):
		error = event_to_error(event, self.view)
		if error is None: return False
		return len(error['gdata']['aSuggestions']) > 0

	# show the suggestion for the error under the mouse
	# or "No suggestion"
	def description(self, event):
		error = event_to_error(event, self.view)
		if len(error['gdata']['aSuggestions']) > 0 :
			return "> " + error['gdata']['aSuggestions'][0] + ""
		else: return "No suggestion"

	# we want to get mouse coordinates
	# when command executed
	def want_event(self):
		return True

# We receive the events from Sublime here
class GrammaEventsCommand(sublime_plugin.EventListener):

	# when the mouse is static for a period of time
	# we show the error message if there is an error
	# under the mouse
	def on_hover(self, view, point, hover_zone):

		# get the plugin state for this view
		state = get_state(view)

		# hide the previous popup
		view.hide_popup()

		# if we're running in this view
		# get and display error message
		if state['showing_gramma']:
			error = point_to_error(point, view)
			if error is not None:
				view.show_popup(error['gdata']['sMessage'], location=point, flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY)

		pass

	## when buffer is modified
	#def on_modified_async(self,view):
	#	global autorun_interval_seconds
	#
	#	print(get_state(view)['next_auto_run']-time.time())
	#
	#	# if we're running
	#	if get_state(view)['showing_gramma']:
	#
	#		# and an autorun is due
	#		if time.time() > get_state(view)['next_auto_run']:
	#
	#			# set next autorun time
	#			get_state(view)['next_auto_run'] = time.time() + autorun_interval_seconds
	#
	#			# run
	#			runGrammalecte(view)

