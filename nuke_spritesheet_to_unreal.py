"""
# write an 2k square sprite sheet sequence
# from image sequence
# in this version the range of the matrix (ej. 5x5)
# is auto generated base on the range of the sequence
"""


from math import sqrt


try:
    inout = nuke.selectedNode()
except:
    inout = None

if inout:
    nroot = nuke.createNode('TimeOffset',inpanel=False)
    
    if nroot.firstFrame() > 1:
        nroot.knob('time_offset').setValue((-nroot.firstFrame())+1)

    nroot.setInput(0,inout)
    nroot.autoplace()
    nroot.setXpos(nroot.xpos())
    nroot.setYpos(inout.ypos()+250)
    
    nroot.selectOnly()
    nroot.setSelected(0)
    
    mrg = nuke.createNode('Merge2',inpanel=False)
    mrg.knob('operation').setValue('plus')
    mrg.setXYpos(nroot.xpos(),nroot.ypos()+150)
    
    nroot.selectOnly()
    nroot.setSelected(0)
    
    innode = nroot.fileDependencies(nroot.lastFrame(),nroot.lastFrame())
    
    if os.name == 'nt':
        name = os.path.splitext(innode[0][1][0])[0].rsplit('.',1)[0].rsplit(os.altsep,1)[1]
    else:
        name = os.path.splitext(innode[0][1][0])[0].rsplit('.',1)[0].rsplit(os.sep,1)[1]
    
    matrix = int(sqrt((inout.lastFrame()-abs(inout.firstFrame()))+1))
    name = 'ue_ss_%ix%i_%s'%(matrix,matrix,name)
    path = os.environ['HOMEPATH']+os.sep+'Documents'+os.sep+'UE_sprites'+os.sep
    
    if os.name == 'nt':
        path = os.environ['HOMEDRIVE']+path.replace(os.sep,os.altsep)

    woutfile = path+name+'.png'
    width = nroot.width()
    height = nroot.height()

    j = 1
    for i in range(matrix**2):
        if not i%matrix:
            j -= 1        
        frmhld = nuke.createNode('FrameHold',inpanel=False)
        frmhld.knob('first_frame').setValue(i+1)
        frmhld.setInput(0,nroot)
        frmhld.autoplace()
        trnsfrm = nuke.createNode('Transform',inpanel=False)
        trnsfrm.knob('translate').setValue((width*(i%matrix),height*j))
        if i > 1:
            mrg.setInput(i+1,trnsfrm)
        else:
            mrg.setInput(i,trnsfrm)
        trnsfrm.autoplace()
        trnsfrm.setSelected(0)
    
    trnsfrm = nuke.createNode('Transform',inpanel=False)
    trnsfrm.knob('translate').setValue((0,height*(matrix-1)))
    trnsfrm.setInput(0,mrg)
    nuke.autoplace_all()
    crp = nuke.createNode('Crop',inpanel=False)
    crp.knob('box').setValue((0,0,width*matrix,height*matrix))
    crp.knob('reformat').setValue(True)
    rfrmt = nuke.createNode('Reformat',inpanel=False)
    rfrmt.knob('type').setValue(1)
    rfrmt.knob('box_width').setValue(width*2)
    nroot.setYpos(nroot.ypos()-50)
    out = nuke.createNode('Write',inpanel=False)
    out.knob('channels').setValue('rgba')
    out.knob('file').setValue(woutfile)
    out.knob('create_directories').setValue(True)
    nroot.selectOnly()
    nroot.setSelected(0)
    nuke.execute(out,1,1)
    nroot.setInput(0,None)
    nroot.selectOnly()
    nuke.selectConnectedNodes()
    nukescripts.node_delete()
    
    del innode,path,woutfile,name,width,height,matrix,inout,nroot,mrg,trnsfrm,crp,rfrmt,out
    del frmhld,j,i
else:
    nuke.message('No Node selected, please select one  :(')
