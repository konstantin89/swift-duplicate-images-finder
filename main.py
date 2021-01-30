from dearpygui import core, simple

from DuplicateImagesManager import DuplicateImagesManager

from View import View

from DuplicateImagesController import DuplicateImagesController

controller = DuplicateImagesController()


controller.Start()

#supported_image_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')


#imageManager = DuplicateImagesManager(supported_image_formats)


#start_scan_callback = lambda scan_directories: imageManager.ScanPaths(scan_directories)

#view = View(start_scan_callback)

#view.Init()

#scan_root = 'C:\\repos_private\\duplicate_images_manager\\img'
#scan_root = 'C:\\'




'''
def apply_selected_file(sender, data):
    print(data)  # so we can see what is inside of data
    directory = data[0]
    file = data[1]

    core.set_value("directory", directory)

    scan_root = directory

    

def file_picker(sender, data):
core.open_file_dialog(callback=apply_selected_file, extensions=".*,.py")

with simple.window("Duplicate Image Scanner"):
    core.add_text("Hello world")
    core.add_button("Start Scan", callback=start_scan)
    core.add_input_text("Scan Root")

    core.add_label_text("##filedir", source="directory", color=[255, 0, 0])

    core.add_button("Directory Selector", callback=file_picker)


core.start_dearpygui()

'''





        
    


