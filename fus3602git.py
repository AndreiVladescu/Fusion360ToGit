import adsk.core, adsk.fusion, adsk.cam, traceback

default_repo_location = 'path_to_git_default_folder'
relative_saving_location = 'path_to_repos_mechanical_section'
model_name = 'model_name'

import adsk.core, adsk.fusion, traceback

output_folder = default_repo_location + relative_saving_location

handlers = []

class MyCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        command = args.command
        command.validateInputs = validateInputs
        command.execute = run

def validateInputs(inputs):
    return True

def run(args):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        exportMgr = design.exportManager

        # Export to IGES
        igesOptions = exportMgr.createIGESExportOptions(output_folder + model_name + '.igs')
        exportMgr.execute(igesOptions)

        # Export to STEP
        stepOptions = exportMgr.createSTEPExportOptions(output_folder + model_name + '.step')
        exportMgr.execute(stepOptions)

        # Export to F3D
        fusionOptions = exportMgr.createFusionArchiveExportOptions(output_folder + model_name + '.f3d')
        exportMgr.execute(fusionOptions)

        ui.messageBox('Design exported successfully to: ' + output_folder)

        # Terminate the script after it finishes running
        adsk.autoTerminate(True)
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def main():
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        commandDefinitions = ui.commandDefinitions
        cmdDef = commandDefinitions.itemById('ExportModel')
        if not cmdDef:
            cmdDef = commandDefinitions.addButtonDefinition('ExportModel', 'Export Model', 'Exports the current model')
        onCommandCreated = MyCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        handlers.append(onCommandCreated)
        cmdDef.execute()
        adsk.autoTerminate(False)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

main()