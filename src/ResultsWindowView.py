from dearpygui import core, simple

from FileMetaData import FileMetaDataList
from FileMetaData import FileMetaData

from core_values_names import NUMBER_OF_SCANNED_IMAGES

class ResultsWindowView:

    def __init__(self, 
        height: int, 
        width:  int,
        x_pos:  int,
        y_pos:  int,
        delete_image_callback: callable,
        delete_all_duplicates_callback: callable):

        self._window_name: str = 'Results Window'

        self._delete_image_callback: callable = delete_image_callback

        self._delete_all_duplicates_callback: callable = delete_all_duplicates_callback


        self._duplicates_list: [FileMetaDataList] = []     

        # RGB color of special text
        self._control_text_color = [0, 200, 255]

        with simple.window(self._window_name):
            core.configure_item(
                self._window_name,
                    width=width,
                    height=height,
                    x_pos=x_pos,
                    y_pos=y_pos,
                    label='Results')



    def ShowWindow(self, duplicates_list):

        self._duplicates_list = duplicates_list

        simple.show_item(self._window_name)

        self._render_results_window()


    def HideWindow(self):

        simple.hide_item(self._window_name)



    def _delete_file_button_click_handler(self, sender: str, file_to_delete: FileMetaData) -> None:
        """ Click handler for the 'Delete File' button.
        """

        # Delete the image
        self._delete_image_callback(file_to_delete.GetPath())

        # Remove the deleted file from duplicates list
        for duplicates_set in self._duplicates_list:

            if file_to_delete in duplicates_set:
                duplicates_set.remove(file_to_delete)
                break

        self._render_results_window()


    def _delete_all_duplicate_click_hander(self, sender, dupicates: [FileMetaDataList]) -> None:
        
        self._duplicates_list = self._delete_all_duplicates_callback(dupicates)
        self._render_results_window()


    def _draw_duplicates_set(self, duplicate_images_list: FileMetaDataList) -> None:
        """ Draw a single image and all the files containing it.
            All the files in duplicate_images_list containg duplicate of same image.
        """
        
        try:

            file_path = duplicate_images_list[0].GetPath()

            core.add_drawing(
                file_path, 
                width=100, 
                height=100, 
                parent=self._window_name)

            core.draw_image(
                file_path, 
                file_path, 
                [0, 0], 
                pmax=[100, 100],
                uv_min=[0, 0], 
                uv_max=[1, 1], 
                tag="image")

            for file in duplicate_images_list:
                
                file_path = file.GetPath()

                core.add_button(
                    'Delete ##'+file_path, 
                    callback=self._delete_file_button_click_handler, 
                    callback_data=file,
                    parent=self._window_name)

                core.add_same_line(parent=self._window_name)

                core.add_text(
                file_path, 
                parent=self._window_name)

            core.add_separator(parent=self._window_name)

        except Exception as e:
            core.log_error('View::_draw_duplicates_set - Exception : [%s]' % (e))
        

    def _render_results_window(self) -> None:

        core.delete_item(item=self._window_name, children_only=True)

        self._render_results_scan_summary()

        self._render_results_group_operations()

        core.add_text(
            'Results', 
            color=self._control_text_color,
            parent=self._window_name)


        for dupicate_image in self._duplicates_list:

            self._draw_duplicates_set(dupicate_image)       


    def _render_results_scan_summary(self):
        """ Present the scan summary
        """

        core.add_text(
            'Scan Summary',
            color=self._control_text_color,
            parent=self._window_name)

        core.add_text(
            'Number of images scanned: ',
            parent=self._window_name)

        core.add_same_line(parent=self._window_name)

        core.add_text(
            name='number_of_scanned_images_text',
            source=NUMBER_OF_SCANNED_IMAGES,
            parent=self._window_name)

        core.add_text(
            'Number duplicate image sets: ',
            parent=self._window_name)

        core.add_same_line(parent=self._window_name)

        core.add_text(
            str(len(self._duplicates_list)),
            parent=self._window_name)

        core.add_text('',  parent=self._window_name)


    def _render_results_group_operations(self):
        """ Render the 'Group Operations' block of 'Results' screen.
        """

        core.add_text(
            name='Group operations',
            color=self._control_text_color,
            parent=self._window_name)

        core.add_button(
            'Keep newest file, delete all other duplicates', 
            callback=self._delete_all_duplicate_click_hander,
            callback_data=self._duplicates_list,
            parent=self._window_name) 

        core.add_text('',  parent=self._window_name)

        core.add_separator(parent=self._window_name)