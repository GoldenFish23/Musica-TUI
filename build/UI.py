"""
This module contains elements of the UI.
"""

class UI:
    """
    This class contains elements of the UI.
    """
    def __init__(self):
        
        # super().__init__()
        self._logo = r"""
  __  __                 _                 
 |  \/  |               (_)                
 | \  / |  _   _   ___   _    ___    __ _  
 | |\/| | | | | | / __| | |  / __|  / _` | 
 | |  | | | |_| | \__ \ | | ( (__  | (_| | 
 |_|  |_|  \__,_| |___/ |_|  \___|  \__,_| 
""".strip("\n")
        self._descriptor = "A Light-weight Terminal Music Player."

    def get_logo(self):
        return self._logo

    def get_descriptor(self):
        return self._descriptor

if __name__ == "__main__":
    ui = UI()
    print(ui.get_logo())
