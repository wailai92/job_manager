from Backend_component.backend_manager import Backend_manager
from UI_component.frontend_manager import UI_Manager

def main():
    main_unit = UI_Manager()
    main_unit.root.page.mainloop()
    
if __name__ == "__main__":
    main()

    