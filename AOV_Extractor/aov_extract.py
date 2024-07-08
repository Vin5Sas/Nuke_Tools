#AOV Extractor v1.0.0
#Python Script by ViSa

import nuke

def extractDefaultAOVList(currentNode):
    layerList = nuke.layers(currentNode)
    layerList.remove("rgb")
    layerList.remove("alpha")
    layerList.sort()

    return layerList

def extractOtherAOVList(currentNode, layerList):
    aovlayers = currentNode.metadata("exr/order")
    
    aov_trunc = aovlayers.replace("{ r g b }","")
    aov_trunc = aov_trunc.replace("{ r g b a }","")
    aov_trunc = aov_trunc.replace("{ x y z }","")
    aov_trunc = aov_trunc.replace("{ u v w }","")

    channel_list = aov_trunc.split()
    channel_list.remove("C")
    channel_list.remove("Pz")
    channel_list.sort()
    
    otherLayers = []

    for channel in channel_list:
        if channel not in layerList:
            otherLayers.append(channel)
    
    return otherLayers

def setDepthShuffle(shuffleNode,aov):
    shuffleNode["in1"].setValue(aov)
    shuffleNode["label"].setValue(aov)
    shuffleNode["out1"].setValue("rgb")
    shuffleNode["mappings"].setValue("depth.Z","rgba.red")
    shuffleNode["mappings"].setValue("depth.Z","rgba.green")
    shuffleNode["mappings"].setValue("depth.Z","rgba.blue")
    
    gradeNode = nuke.createNode("Grade", inpanel = False)
    gradeNode.setInput(0,shuffleNode)
    copyNode = nuke.createNode("Copy", inpanel = False)
    copyNode.setInput(1,gradeNode)
    copyNode.setInput(0,gradeNode)
    copyNode["from0"].setValue("rgba.red")
    copyNode["to0"].setValue("rgba.alpha")

def setXYZShuffle(shuffleNode, aov):
    shuffleNode["out1"].setValue("rgb")
    shuffleNode["mappings"].setValue(aov+".x","rgba.red")
    shuffleNode["mappings"].setValue(aov+".y","rgba.green")
    shuffleNode["mappings"].setValue(aov+".z","rgba.blue")

def mapOtherAOV(shuffleNode, aov):
    shuffleNode["label"].setValue(aov)
    shuffleNode["mappings"].setValue("other."+aov,"rgba.red")
    shuffleNode["mappings"].setValue("other."+aov,"rgba.green")
    shuffleNode["mappings"].setValue("other."+aov,"rgba.blue")   
    
def createShuffleNode(aov, current_node):
    
    floatAOV_List = ['depth','N','P']
    
    shuffleNode = nuke.createNode("Shuffle2", inpanel = False)
    shuffleNode["in1"].setValue(aov)
    shuffleNode["postage_stamp"].setValue(True)
    shuffleNode["label"].setValue(aov)
    shuffleNode.setInput(0,current_node)

    if any([aov==float_aov for float_aov in floatAOV_List]):
        if aov=='P':
            setXYZShuffle(shuffleNode,aov)
        elif aov=='depth':
            setDepthShuffle(shuffleNode,aov)
        elif aov=='N':
            setXYZShuffle(shuffleNode,aov)
        else:
            pass
    
    return shuffleNode

def createOtherAOVShuffles(otherLayers, current_node):
    for i in range(len(otherLayers)):
        otherAOVshuffle = createShuffleNode("other", current_node)
        mapOtherAOV(otherAOVshuffle, otherLayers[i])
       

####MAIN

def performExtractAOV():
    current_node = nuke.selectedNode()
    current_node_name = current_node.name()

    if 'read' in current_node_name.lower():
    
        aov_list = extractDefaultAOVList(current_node)
        otherLayers = extractOtherAOVList(current_node, aov_list)
    
        if "other" in aov_list:
            aov_list.remove("other")
            createOtherAOVShuffles(otherLayers, current_node)
        
        for aov in aov_list:
            shuffle_node = createShuffleNode(aov, current_node)
        
        nuke.autoplace_all()
    
    else:
        nuke.message("Please select a valid Read node to extract AOVs from")

#performExtractAOV()
nuke.autoplace_all()
#OUTPUT