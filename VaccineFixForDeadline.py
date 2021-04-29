from System.IO import *
import os,pickle
import os.path

from System.Collections.Specialized import *
from System.IO import *
from System.Text import *

from Deadline.Scripting import *
from DeadlineUI.Controls.Scripting.DeadlineScriptDialog import DeadlineScriptDialog

########################################################################
## Globals
########################################################################
scriptDialog = None
settings = None


########################################################################
## Main Function Called By Deadline
########################################################################
def __main__():
    global scriptDialog
    global settings

    scriptDialog = DeadlineScriptDialog()
    scriptDialog.SetTitle( "Vaccine fix" )

    scriptDialog.AddTabControl( "Example Tab Control", 0, 0 )

    scriptDialog.AddTabPage( "Job Options" )
    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid( "Separator1", "SeparatorControl", "Job Description", 0, 0, colSpan=2 )

    scriptDialog.AddControlToGrid( "NameLabel", "LabelControl", "Job Name", 1, 0, "The name of your job. This is optional, and if left blank, it will default to 'Untitled'.", False )
    scriptDialog.AddControlToGrid( "NameBox", "TextControl", "Vaccine_patch", 1,1 )

    scriptDialog.AddControlToGrid( "CommentLabel", "LabelControl", "Comment", 2, 0, "A simple description of your job. This is optional and can be left blank.", False )
    scriptDialog.AddControlToGrid( "CommentBox", "TextControl", "", 2, 1 )

    scriptDialog.AddControlToGrid( "DepartmentLabel", "LabelControl", "Department", 3, 0, "The department you belong to. This is optional and can be left blank.", False )
    scriptDialog.AddControlToGrid( "DepartmentBox", "TextControl", "", 3, 1 )
    scriptDialog.EndGrid()

    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid( "Separator2", "SeparatorControl", "Job Options", 0, 0, colSpan=3 )

    scriptDialog.AddControlToGrid( "PoolLabel", "LabelControl", "Pool", 1, 0, "The pool that your job will be submitted to.", False )
    scriptDialog.AddControlToGrid( "PoolBox", "PoolComboControl", "ffmpeg", 1, 1 )

    scriptDialog.AddControlToGrid( "MachineListLabel", "LabelControl", "Machine List", 2, 0, "The whitelisted or blacklisted list of machines.", False )
    scriptDialog.AddControlToGrid( "MachineListBox", "MachineListControl", "", 2, 1, colSpan=2 )


    temp_in = "Y:\\TOOLS\\EmerTech\\vaccine_patch"

    scriptDialog.AddControlToGrid( "VersionLabel", "LabelControl", "Maya Version", 3, 0, "The version of Maya to render with.", False )
    versionBox = scriptDialog.AddComboControlToGrid( "VersionBox", "ComboControl", "2019", ("2010","2011","2011.5","2012","2012.5","2013","2013.5","2014","2014.5","2015","2015.5","2016","2016.5","2017","2017.5","2018","2019"), 3, 1 )
    #versionBox.ValueModified.connect( VersionChanged )

    scriptDialog.AddControlToGrid("OutputLabel", "LabelControl", "Patch File", 4, 0, "python patch file path.", False)
    scriptDialog.AddSelectionControlToGrid("Input0Box", "FolderBrowserControl", temp_in,"", 4,1)

    scriptDialog.EndGrid()
    scriptDialog.EndTabPage()

    scriptDialog.EndTabControl()

    scriptDialog.AddGrid()
    submitButton = scriptDialog.AddControlToGrid("SubmitButton", "ButtonControl", "Submit", 0, 1, expand=False)
    submitButton.ValueModified.connect(SubmitButtonPressed)
    closeButton = scriptDialog.AddControlToGrid( "CloseButton", "ButtonControl", "Close", 0, 2, expand=False )
    closeButton.ValueModified.connect( CloseButtonPressed )
    scriptDialog.AddHorizontalSpacerToGrid("DummySpacer1", 0, 3 )
    scriptDialog.EndGrid()

    scriptDialog.ShowDialog( True )

########################################################################
## Helper Functions
########################################################################


def CloseButtonPressed( *args ):
    global scriptDialog
    scriptDialog.CloseDialog()


def SubmitButtonPressed(*args):
    global scriptDialog
    import datetime
    now = datetime.datetime.now()
    machine_list = scriptDialog.GetValue("MachineListBox").strip().split(',')
    project_file_path = scriptDialog.GetValue("Input0Box").strip()
    patch_file = project_file_path +'\\patch.py'
    scene_file = project_file_path +'\\empty_scene.ma'
    batchName = scriptDialog.GetValue("NameBox") + '_' + now.strftime("%Y-%m-%d_%H:%M:%S")
    if not os.path.isdir(project_file_path):
        scriptDialog.ShowMessageBox("Please select the patch folder", "Error")
        return
    if not os.path.isfile(patch_file):
        scriptDialog.ShowMessageBox("Could not find path.py", "Error")
        return
    if not os.path.isfile(scene_file):
        scriptDialog.ShowMessageBox("Could not find empty_scene.ma", "Error")
        return
    if not machine_list:
        scriptDialog.ShowMessageBox("Please choose machine list", "Error")
        return
    for machine in machine_list:
        jobInfoFilename = Path.Combine(ClientUtils.GetDeadlineTempPath(), machine+"_job_info.job")
        writer = StreamWriter(jobInfoFilename, False, Encoding.Unicode)
        writer.WriteLine("Plugin=MayaBatch")

        writer.WriteLine("Name=%s" % machine + '_vaccine_patch')
        writer.WriteLine("Comment=%s" % scriptDialog.GetValue("CommentBox"))
        writer.WriteLine("Department=%s" % scriptDialog.GetValue("DepartmentBox"))
        writer.WriteLine("Pool=%s" % scriptDialog.GetValue("PoolBox"))
        writer.WriteLine("SecondaryPool=")
        writer.WriteLine("Group=none")
        writer.WriteLine("Priority=99")
        writer.WriteLine("TaskTimeoutMinutes=0")
        writer.WriteLine("EnableAutoTimeout=False")
        writer.WriteLine("ConcurrentTasks=1")
        writer.WriteLine("LimitConcurrentTasksToNumberOfCpus=True")
        writer.WriteLine("MachineLimit=0")
        writer.WriteLine("Whitelist=%s" % machine)
        writer.WriteLine("LimitGroups=")
        writer.WriteLine("JobDependencies=")
        writer.WriteLine("OnJobComplete=Nothing")
        writer.WriteLine("Frames=0")
        writer.WriteLine("ChunkSize=1")
        writer.WriteLine("BatchName=%s" % batchName)
        writer.Close()

        # Create plugin info file.
        pluginInfoFilename = Path.Combine(ClientUtils.GetDeadlineTempPath(), machine + "_plugin_info.job")
        writer = StreamWriter(pluginInfoFilename, False, Encoding.Unicode)
        writer.WriteLine("SceneFile=%s" % scene_file)
        writer.WriteLine("Version=%s" % scriptDialog.GetValue("VersionBox"))
        writer.WriteLine("Build=none")
        writer.WriteLine("ProjectPath=%s" %project_file_path)
        writer.WriteLine("StrictErrorChecking=True")
        writer.WriteLine("UseLegacyRenderLayers=0")
        writer.WriteLine("RenderSetupIncludeLights=1")
        writer.WriteLine("ScriptJob=True")
        writer.WriteLine("ScriptFilename=patch.py")
        writer.Close()
        arguments = StringCollection()
        arguments.Add(jobInfoFilename)
        arguments.Add(pluginInfoFilename)
        arguments.Add(patch_file)
        results = ClientUtils.ExecuteCommandAndGetOutput(arguments)
    scriptDialog.ShowMessageBox("submitted",
                                    "Submission Results")







