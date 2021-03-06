spm('defaults', 'fmri');
spm_jobman('initcfg');
matlabbatch{1}.spm.tools.cat.estwrite.data = {'$DATA_PATH,1'};
matlabbatch{1}.spm.tools.cat.estwrite.data_wmh = {''};
matlabbatch{1}.spm.tools.cat.estwrite.nproc = $N_PROCESSES;
matlabbatch{1}.spm.tools.cat.estwrite.useprior = '';
matlabbatch{1}.spm.tools.cat.estwrite.opts.tpm = {'$TPM_PATH'};
matlabbatch{1}.spm.tools.cat.estwrite.opts.affreg = '$AFFINE_REGULARISATION';
matlabbatch{1}.spm.tools.cat.estwrite.opts.biasstr = $BIAS_STRENGTH;
matlabbatch{1}.spm.tools.cat.estwrite.extopts.APP = $AFFINE_PREPROCESSING;
matlabbatch{1}.spm.tools.cat.estwrite.extopts.spm_kamap = $INITIAL_SEGMENTATION;
matlabbatch{1}.spm.tools.cat.estwrite.extopts.LASstr = $LOCAL_ADAPTIVE_SEGMENTATION_STRENGTH;
matlabbatch{1}.spm.tools.cat.estwrite.extopts.gcutstr = $SKULL_STRIPPING;
matlabbatch{1}.spm.tools.cat.estwrite.extopts.registration.shooting.shootingtpm = {'$SHOOTING_TPM_PATH'};
matlabbatch{1}.spm.tools.cat.estwrite.extopts.registration.shooting.regstr = $SHOOTING_STRENGTH;
matlabbatch{1}.spm.tools.cat.estwrite.extopts.vox = $NORMALIZED_IMAGE_VOXEL_SIZE;
matlabbatch{1}.spm.tools.cat.estwrite.extopts.restypes.optimal = [1 0.1];
matlabbatch{1}.spm.tools.cat.estwrite.output.surface = $SURFACE_ESTIMATION;
matlabbatch{1}.spm.tools.cat.estwrite.output.surf_measures = 1;
matlabbatch{1}.spm.tools.cat.estwrite.output.ROImenu.atlases.neuromorphometrics = $NEUROMORPHOMETRICS;
matlabbatch{1}.spm.tools.cat.estwrite.output.ROImenu.atlases.lpba40 = $LPBA40;
matlabbatch{1}.spm.tools.cat.estwrite.output.ROImenu.atlases.cobra = $COBRA;
matlabbatch{1}.spm.tools.cat.estwrite.output.ROImenu.atlases.hammers = $HAMMERS;
matlabbatch{1}.spm.tools.cat.estwrite.output.ROImenu.atlases.ownatlas = {''};
matlabbatch{1}.spm.tools.cat.estwrite.output.GM.native = $NATIVE_GREY_MATTER;
matlabbatch{1}.spm.tools.cat.estwrite.output.GM.mod = $MODULATED_GREY_MATTER;
matlabbatch{1}.spm.tools.cat.estwrite.output.GM.dartel = $DARTEL_GREY_MATTER;
matlabbatch{1}.spm.tools.cat.estwrite.output.WM.native = $NATIVE_WHITE_MATTER;
matlabbatch{1}.spm.tools.cat.estwrite.output.WM.mod = $MODULATED_WHITE_MATTER;
matlabbatch{1}.spm.tools.cat.estwrite.output.WM.dartel = $DARTEL_WHITE_MATTER
matlabbatch{1}.spm.tools.cat.estwrite.output.CSF.native = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.CSF.warped = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.CSF.mod = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.CSF.dartel = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.ct.native = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.ct.warped = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.ct.dartel = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.pp.native = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.pp.warped = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.pp.dartel = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.WMH.native = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.WMH.warped = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.WMH.mod = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.WMH.dartel = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.SL.native = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.SL.warped = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.SL.mod = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.SL.dartel = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.TPMC.native = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.TPMC.warped = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.TPMC.mod = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.TPMC.dartel = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.atlas.native = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.atlas.warped = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.atlas.dartel = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.label.native = 1;
matlabbatch{1}.spm.tools.cat.estwrite.output.label.warped = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.label.dartel = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.labelnative = $NATIVE_PVE;
matlabbatch{1}.spm.tools.cat.estwrite.output.bias.warped = $WARPED_IMAGE;
matlabbatch{1}.spm.tools.cat.estwrite.output.las.native = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.las.warped = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.las.dartel = 0;
matlabbatch{1}.spm.tools.cat.estwrite.output.jacobianwarped = $JACOBIAN_DETERMINANT;
matlabbatch{1}.spm.tools.cat.estwrite.output.warps = $DEFORMATION_FIELDS;
spm_jobman('run', matlabbatch);