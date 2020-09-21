spm('defaults', 'fmri');
spm_jobman('initcfg');
matlabbatch{1}.spm.tools.cat.long.datalong.subjects = {
                                                       {
                                                       $T1W_SCANS
                                                       }
                                                       };
matlabbatch{1}.spm.tools.cat.long.longmodel = $LONGITUDINAL_MODEL;
matlabbatch{1}.spm.tools.cat.long.nproc = $N_PROCESSES;
matlabbatch{1}.spm.tools.cat.long.opts.tpm = {'$TPM_PATH'};
matlabbatch{1}.spm.tools.cat.long.opts.affreg = 'mni';
matlabbatch{1}.spm.tools.cat.long.opts.biasstr = $BIAS_STRENGTH;
matlabbatch{1}.spm.tools.cat.long.extopts.APP = $AFFINE_PREPROCESSING;
matlabbatch{1}.spm.tools.cat.long.extopts.spm_kamap = $INITIAL_SEGMENTATION;
matlabbatch{1}.spm.tools.cat.long.extopts.LASstr = $LOCAL_ADAPTIVE_SEGMENTATION_STRENGTH;
matlabbatch{1}.spm.tools.cat.long.extopts.gcutstr = $SKULL_STRIPPING;
matlabbatch{1}.spm.tools.cat.long.extopts.registration.shooting.shootingtpm = {'$SHOOTING_TPM_PATH'};
matlabbatch{1}.spm.tools.cat.long.extopts.registration.shooting.regstr = $SHOOTING_STRENGTH;
matlabbatch{1}.spm.tools.cat.long.extopts.vox = $NORMALIZED_IMAGE_VOXEL_SIZE;
matlabbatch{1}.spm.tools.cat.long.extopts.restypes.optimal = [1 0.1];
matlabbatch{1}.spm.tools.cat.long.output.surface = $SURFACE_ESTIMATION;
matlabbatch{1}.spm.tools.cat.long.ROImenu.atlases.neuromorphometrics = $NEUROMORPHOMETRICS;
matlabbatch{1}.spm.tools.cat.long.ROImenu.atlases.lpba40 = $LPBA40;
matlabbatch{1}.spm.tools.cat.long.ROImenu.atlases.cobra = $COBRA;
matlabbatch{1}.spm.tools.cat.long.ROImenu.atlases.hammers = $HAMMERS;
matlabbatch{1}.spm.tools.cat.long.ROImenu.atlases.ownatlas = {''};
matlabbatch{1}.spm.tools.cat.long.modulate = 1;
matlabbatch{1}.spm.tools.cat.long.dartel = 0;
matlabbatch{1}.spm.tools.cat.long.delete_temp = 1;
spm_jobman('run', matlabbatch);