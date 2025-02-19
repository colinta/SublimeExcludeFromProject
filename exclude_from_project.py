import sublime
import sublime_plugin
import json
import os


class ExcludeFromProjectCommand(sublime_plugin.WindowCommand):
    def run(self, paths):
        if not paths:
            return

        success_paths = []
        for path in paths:
            if self.run_each(path):
                success_paths.append(path)
        if success_paths:
            sublime.status_message("Added {} path(s) to project exclusions".format(len(success_paths)))

    def run_each(self, path):
        # Get the current project file path
        project_data = self.window.project_data()
        project_file = self.window.project_file_name()

        if not project_data or not project_file:
            sublime.error_message("No project file found. Please save your project first.")
            return False

        # find the folder in project_data['folders'] that contains the path
        folder_settings = None
        for f in project_data['folders']:
            # if f['path'] is a prefix of path, that's the folder
            if path.startswith(f['path']):
                folder_settings = f
                break

        if not folder_settings:
            sublime.error_message("Path '{}' is not in a project folder.".format(path))
            return False

        # Initialize folder_exclude_patterns if it doesn't exist
        if 'folder_exclude_patterns' not in folder_settings:
            folder_settings['folder_exclude_patterns'] = []

        # Get the project root directory
        project_root = os.path.dirname(project_file)

        if path not in folder_settings['folder_exclude_patterns']:
            folder_settings['folder_exclude_patterns'].append(path)

        # Save the updated project data
        self.window.set_project_data(project_data)
        return True

    def is_visible(self, paths):
        # Only show the command if we have a project file
        return bool(self.window.project_file_name())


class EditProjectFileCommand(sublime_plugin.WindowCommand):
    def run(self):
        project_file = self.window.project_file_name()
        if project_file:
            self.window.open_file(project_file)
        else:
            sublime.error_message("No project file found. Please save your project first.")

    def is_visible(self):
        return bool(self.window.project_file_name())
