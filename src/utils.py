import webbrowser

from dearpygui import core, simple
 
 
GITHUB_LINK:str = 'https://github.com/konstantin89/swift-duplicate-images-finder'

def visit_source_web_page():
    """
    """

    try:
        webbrowser.open(GITHUB_LINK, new=2)

    except Exception as e:
        core.log_error('HelloScreenView - Failed to visit source page with exception : [%s]' % (e))