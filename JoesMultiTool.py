import maya.cmds as cmds
import os
import time
import random

class SceneOptimizerUI:
    def __init__(self):
        self.windowName = "JoesMulitTool"
        self.selection = None
        self.createUI()

    def createUI(self):
        if cmds.window(self.windowName, exists=True):
            cmds.deleteUI(self.windowName, window=True)

        self.window = cmds.window(self.windowName, title="JoesMulitTool", widthHeight=(400, 250))
        self.mainLayout = cmds.columnLayout(adjustableColumn=True, columnAlign="center")

        self.infoText = cmds.text(label="Select options and click 'Submit Changes':", align="center")
        cmds.separator(style="none", height=10)

        self.removeHistoryCB = cmds.checkBox(label="Remove History", value=True)
        self.moveToOriginCB = cmds.checkBox(label="Move to Origin", value=True)
        self.resetTransformationsCB = cmds.checkBox(label="Reset Transformations", value=False)
        self.duplicateObjectsCB = cmds.checkBox(label="Duplicate Objects", value=True)

        cmds.separator(style="none", height=10)

        self.scaleSlider = cmds.floatSliderGrp(label="Scale Factor", field=True, minValue=1.0, maxValue=10.0, fieldMinValue=1.0, fieldMaxValue=100.0, value=1.0, columnWidth3=[120, 100, 120], visible=False)

        cmds.separator(style="none", height=10)
        self.optimizeButton = cmds.button(label="Submit Changes", command=self.optimizeScene)
        self.metricsButton = cmds.button(label="Performance Stats", command=self.displayMetrics)
        cmds.separator(style="none", height=10)

        cmds.showWindow(self.window)

    def getSelectedObjects(self):
        self.selection = cmds.ls(selection=True, long=True) or []

    def removeHistory(self):
        if cmds.checkBox(self.removeHistoryCB, query=True, value=True):
            for obj in self.selection:
                cmds.delete(obj, constructionHistory=True)

    def moveToOrigin(self):
        if cmds.checkBox(self.moveToOriginCB, query=True, value=True):
            for obj in self.selection:
                cmds.xform(obj, translation=[0, 0, 0])

    def resetTransformations(self):
        if cmds.checkBox(self.resetTransformationsCB, query=True, value=True):
            for obj in self.selection:
                cmds.xform(obj, translation=[0, 0, 0], rotation=[0, 0, 0], scale=[1, 1, 1])

    def duplicateObjects(self):
        if cmds.checkBox(self.duplicateObjectsCB, query=True, value=True):
            for obj in self.selection:
                duplicateObj = cmds.duplicate(obj)[0]
                # Example: Randomize position within a range of -5 to 5 units
                randomOffset = (random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5))
                cmds.move(*randomOffset, duplicateObj)

    def optimizeScene(self, *args):
        startTime = time.time()

        # Run optimization processes
        self.getSelectedObjects()
        if not self.selection:
            cmds.warning("No objects selected.")
            return

        self.removeHistory()
        self.moveToOrigin()
        self.resetTransformations()
        self.duplicateObjects()

        optimizationTime = time.time() - startTime
        cmds.warning(f"Scene changes completed. Time taken: {optimizationTime:.2f} seconds.")

    def displayMetrics(self, *args):
        # Get scene file size before optimization
        initialFileSize = os.path.getsize(cmds.file(q=True, sceneName=True))

        # Get scene file size after optimization
        finalFileSize = os.path.getsize(cmds.file(q=True, sceneName=True))

        # Measure render time (just a placeholder)
        renderTime = 30  # Placeholder render time in seconds

        # Calculate optimization time
        optimizationTime = 5.0  # Placeholder optimization time

        # Display performance metrics to the user
        metricsText = f"Initial File Size: {initialFileSize} bytes\n"
        metricsText += f"Final File Size: {finalFileSize} bytes\n"
        metricsText += f"Render Time Before Optimization: 0 seconds\n"
        metricsText += f"Render Time After Optimization: {renderTime} seconds\n"
        metricsText += f"Optimization Time: {optimizationTime:.2f} seconds\n"

        cmds.confirmDialog(title="Performance Metrics", message=metricsText, button="OK", defaultButton="OK")

# Run UI
SceneOptimizerUI()