#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 14:04:17 2024

@author: colin
"""

import os
from os.path import join as pjoin
from os.path import exists as pexists
import sys
import subprocess
import argparse
import time


def bids_registration(bids, sub, ses, input_path, ref_path, deriv=None, reg_name=None, quick=True):
    
    print('Registration')
    # 1. find reg-name
    input_p, input_f = rename_path_sub_ses(bids, sub, ses, input_path)
    ref_p, ref_f = rename_path_sub_ses(bids, sub, ses, ref_path)
    
    reg_space = ''
    out_name = ''
    if not reg_name:
        print('not reg_name')
        ref_d = ref_f.split('.')[0].split('_')
        reg_space = f'reg-{ref_d[-1]}'
        input_d = input_f.split('.')[0].split('_')
        input_d.insert(-1, reg_space)
        out_name = '_'.join(input_d)
    
    else:
        print('reg_name')
        reg_space = reg_name
        input_d = input_f.split('.')[0].split('_')
        input_d.insert(-1, reg_space)
        out_name = '_'.join(input_d)
        
    if not deriv:
        print('not deriv')
        deriv = f'registrations/{reg_space}'
    
    sub_ses_deriv = pjoin(bids, 'derivatives', deriv, f'sub-{sub}', f'ses-{ses}')
        
    os.makedirs(sub_ses_deriv, exist_ok=True)
    
    if quick:
        print('Quick!')
        print('Command:', f"antsRegistrationSyNQuick.sh -f {pjoin(ref_p, ref_f)} -m {pjoin(input_p, input_f)} -t r -o {pjoin(sub_ses_deriv, out_name)}")
        subprocess.Popen(f"antsRegistrationSyNQuick.sh -f {pjoin(ref_p, ref_f)} -m {pjoin(input_p, input_f)} -t r -o {pjoin(sub_ses_deriv, out_name)}", shell=True).wait()

    else:
        print('Extended registration')
        print('Command:', f"antsRegistrationSyN.sh -f {pjoin(ref_p, ref_f)} -m {pjoin(input_p, input_f)} -t r -o {pjoin(sub_ses_deriv, out_name)}")
        subprocess.Popen(f"antsRegistrationSyN.sh -f {pjoin(ref_p, ref_f)} -m {pjoin(input_p, input_f)} -t r -o {pjoin(sub_ses_deriv, out_name)}", shell=True).wait()
    
    if pexists(pjoin(sub_ses_deriv, f'{out_name}Warped.nii.gz')):
        os.rename(pjoin(sub_ses_deriv, f'{out_name}Warped.nii.gz'), pjoin(sub_ses_deriv, f'{out_name}.nii.gz'))
        os.remove(pjoin(sub_ses_deriv, f'{out_name}InverseWarped.nii.gz'))
    else:
        print('[ERROR] issue during registration')
        return pjoin(sub_ses_deriv, out_name)
        
    return pjoin(sub_ses_deriv, out_name)
    
  
def bids_registration_docker(bids, sub, ses, input_path, ref_path, deriv=None, reg_name=None, quick=True):
    
    print('Registration')
    # 1. find reg-name
    input_p, input_f = rename_path_sub_ses(bids, sub, ses, input_path)
    ref_p, ref_f = rename_path_sub_ses(bids, sub, ses, ref_path)
    
    reg_space = ''
    out_name = ''
    if not reg_name:
        print('not reg_name')
        ref_d = ref_f.split('.')[0].split('_')
        reg_space = f'reg-{ref_d[-1]}'
        input_d = input_f.split('.')[0].split('_')
        input_d.insert(-1, reg_space)
        out_name = '_'.join(input_d)
    
    else:
        print('reg_name')
        reg_space = reg_name
        input_d = input_f.split('.')[0].split('_')
        input_d.insert(-1, reg_space)
        out_name = '_'.join(input_d)
        
    if not deriv:
        print('not deriv')
        deriv = f'registrations/{reg_space}'
    
    sub_ses_deriv = pjoin(bids, 'derivatives', deriv, f'sub-{sub}', f'ses-{ses}')
    
    os.makedirs(sub_ses_deriv, exist_ok=True)
    
    if quick:
        print('Quick!')
        print('Command:', f"docker run --rm --privileged -v {input_p}:/media/input -v {ref_p}:/media/ref -v {sub_ses_deriv}:/media/output antsx/ants antsRegistrationSyNQuick.sh -f {pjoin('/media/ref', ref_f)} -m {pjoin('/media/input', input_f)} -t r -o {pjoin('/media/output', out_name)}")
        subprocess.Popen(f"docker run --rm --privileged -v {input_p}:/media/input -v {ref_p}:/media/ref -v {sub_ses_deriv}:/media/output antsx/ants antsRegistrationSyNQuick.sh -f {pjoin('/media/ref', ref_f)} -m {pjoin('/media/input', input_f)} -t r -o {pjoin('/media/output', out_name)}", shell=True).wait()
    else:
        print('Extended registration')
        print('Command:', f"docker run --rm --privileged -v {input_p}:/media/input -v {ref_p}:/media/ref -v {sub_ses_deriv}:/media/output antsx/ants antsRegistrationSyN.sh -f {pjoin('/media/ref', ref_f)} -m {pjoin('/media/input', input_f)} -t r -o {pjoin('/media/output', out_name)}")
        subprocess.Popen(f"docker run --rm --privileged -v {input_p}:/media/input -v {ref_p}:/media/ref -v {sub_ses_deriv}:/media/output antsx/ants antsRegistrationSyN.sh -f {pjoin('/media/ref', ref_f)} -m {pjoin('/media/input', input_f)} -t r -o {pjoin('/media/output', out_name)}", shell=True).wait()
        
    print('docker has finished')
    
    if pexists(pjoin(sub_ses_deriv, f'{out_name}Warped.nii.gz')):
        os.rename(pjoin(sub_ses_deriv, f'{out_name}Warped.nii.gz'), pjoin(sub_ses_deriv, f'{out_name}.nii.gz'))
        os.remove(pjoin(sub_ses_deriv, f'{out_name}InverseWarped.nii.gz'))
    else:
        print('[ERROR] issue during registration')
        return pjoin(sub_ses_deriv, out_name)
    
    return pjoin(sub_ses_deriv, out_name)


def bids_apply_transforms(bids, sub, ses, input_path, ref_path, trans_mat, deriv=None, reg_name=None, label=False, inverse=False):
    
    print('Apply Transform')
    # 1. find reg-name
    input_p, input_f = rename_path_sub_ses(bids, sub, ses, input_path)
    ref_p, ref_f = rename_path_sub_ses(bids, sub, ses, ref_path)
    trans_mat_p, trans_mat_f = rename_path_sub_ses(bids, sub, ses, trans_mat)
    
    reg_space = ''
    out_name = ''
    if not reg_name:
        print('not reg_name')
        trans_mat_d = trans_mat_f.split('.')[0].split('_')
        reg_space = trans_mat_d[-2]
        input_d = input_f.split('.')[0].split('_')
        input_d.insert(-1, reg_space)
        out_name = '_'.join(input_d)
    
    else:
        print('reg_name')
        reg_space = reg_name
        input_d = input_f.split('.')[0].split('_')
        input_d.insert(-1, reg_space)
        out_name = '_'.join(input_d)
        
    if not deriv:
        print('not deriv')
        deriv = f'registrations/{reg_space}'
    
    sub_ses_deriv = pjoin(bids, 'derivatives', deriv, f'sub-{sub}', f'ses-{ses}')
    
    os.makedirs(sub_ses_deriv, exist_ok=True)
    
    interpolator = 'GenreicLabel' if label else 'Linear'
    print(f'{interpolator=}')
    
    if inverse:
        print('use inverse')
        print('Command:', f"antsApplyTransforms -i {pjoin(input_p, input_f)} -r {pjoin(ref_p, ref_f)} -n {interpolator} -t [{pjoin(trans_mat_p, trans_mat_f)},1] -o {pjoin(sub_ses_deriv, f'{out_name}.nii.gz')}")
        subprocess.Popen(f"antsApplyTransforms -i {pjoin(input_p, input_f)} -r {pjoin(ref_p, ref_f)} -n {interpolator} -t [{pjoin(trans_mat_p, trans_mat_f)},1] -o {pjoin(sub_ses_deriv, f'{out_name}.nii.gz')}", shell=True).wait()
    else:
        print('Command:', f"antsApplyTransforms -i {pjoin(input_p, input_f)} -r {pjoin(ref_p, ref_f)} -n {interpolator} -t {pjoin(trans_mat_p, trans_mat_f)} -o {pjoin(sub_ses_deriv, f'{out_name}.nii.gz')}")
        subprocess.Popen(f"antsApplyTransforms -i {pjoin(input_p, input_f)} -r {pjoin(ref_p, ref_f)} -n {interpolator} -t {pjoin(trans_mat_p, trans_mat_f)} -o {pjoin(sub_ses_deriv, f'{out_name}.nii.gz')}", shell=True).wait()
    
    
    
def bids_apply_transforms_docker(bids, sub, ses, input_path, ref_path, trans_mat, deriv=None, reg_name=None, label=False, inverse=False):
    
    print('Apply Transform')
    # 1. find reg-name
    input_p, input_f = rename_path_sub_ses(bids, sub, ses, input_path)
    ref_p, ref_f = rename_path_sub_ses(bids, sub, ses, ref_path)
    trans_mat_p, trans_mat_f = rename_path_sub_ses(bids, sub, ses, trans_mat)
    
    reg_space = ''
    out_name = ''
    if not reg_name:
        print('not reg_name')
        trans_mat_d = trans_mat_f.split('.')[0].split('_')
        reg_space = trans_mat_d[-2]
        input_d = input_f.split('.')[0].split('_')
        input_d.insert(-1, reg_space)
        out_name = '_'.join(input_d)
    
    else:
        print('reg_name')
        reg_space = reg_name
        input_d = input_f.split('.')[0].split('_')
        input_d.insert(-1, reg_space)
        out_name = '_'.join(input_d)
        
    if not deriv:
        print('not deriv')
        deriv = f'registrations/{reg_space}'
    
    sub_ses_deriv = pjoin(bids, 'derivatives', deriv, f'sub-{sub}', f'ses-{ses}')
    
    os.makedirs(sub_ses_deriv, exist_ok=True)
    
    interpolator = 'GenreicLabel' if label else 'Linear'
    print(f'{interpolator=}')
    
    if inverse:
        print('use inverse')
        print('Command:', f"docker run --rm --privileged -v {input_p}:/media/input -v {ref_p}:/media/ref -v {trans_mat_p}:/media/trans_mat -v {sub_ses_deriv}:/media/output antsx/ants antsApplyTransforms -i {pjoin('/media/input', input_f)} -r {pjoin('/media/ref', ref_f)} -n {interpolator} -t [{pjoin('/media/trans_mat', trans_mat_f)},1] -o {pjoin('/media/output', f'{out_name}.nii.gz')}")
        subprocess.Popen(f"docker run --rm --privileged -v {input_p}:/media/input -v {ref_p}:/media/ref -v {trans_mat_p}:/media/trans_mat -v {sub_ses_deriv}:/media/output antsx/ants antsApplyTransforms -i {pjoin('/media/input', input_f)} -r {pjoin('/media/ref', ref_f)} -n {interpolator} -t [{pjoin('/media/trans_mat', trans_mat_f)},1] -o {pjoin('/media/output', f'{out_name}.nii.gz')}", shell=True).wait()
    else:
        print('Command:', f"docker run --rm --privileged -v {input_p}:/media/input -v {ref_p}:/media/ref -v {trans_mat_p}:/media/trans_mat -v {sub_ses_deriv}:/media/output antsx/ants antsApplyTransforms -i {pjoin('/media/input', input_f)} -r {pjoin('/media/ref', ref_f)} -n {interpolator} -t {pjoin('/media/trans_mat', trans_mat_f)} -o {pjoin('/media/output', f'{out_name}.nii.gz')}")
        subprocess.Popen(f"docker run --rm --privileged -v {input_p}:/media/input -v {ref_p}:/media/ref -v {trans_mat_p}:/media/trans_mat -v {sub_ses_deriv}:/media/output antsx/ants antsApplyTransforms -i {pjoin('/media/input', input_f)} -r {pjoin('/media/ref', ref_f)} -n {interpolator} -t {pjoin('/media/trans_mat', trans_mat_f)} -o {pjoin('/media/output', f'{out_name}.nii.gz')}", shell=True).wait()
   

    
def rename_path_sub_ses(bids, sub, ses, path):
    """


    Parameters
    ----------
    path : TYPE
        DESCRIPTION.
    sub : TYPE
        DESCRIPTION.
    ses : TYPE
        DESCRIPTION.

    Returns
    -------
    path_name : TYPE
        DESCRIPTION.

    """

    if not is_subpath(path, bids):
        print('[ERROR] path selected not in the BIDS directory')
        return
    
    rel_path = os.path.relpath(path, bids).split(os.sep)
    file = rel_path[-1]
    new_path = []
    for p in rel_path[:-1]:
        if 'sub-' in p:
            new_path.append(f'sub-{sub}')
        elif 'ses-' in p:
            new_path.append(f'ses-{ses}')
        else:
            new_path.append(p)
    new_file = []
    for k in file.split('_'):
        if 'sub-' in k:
            new_file.append(f'sub-{sub}')
        elif'ses-' in k:
            new_file.append(f'ses-{ses}')
        else:
            new_file.append(k)
    return pjoin(bids, *new_path), '_'.join(new_file)
    

def get_out_name(bids, sub, ses, input_path, ref_path, deriv=None, reg_name=None):
    
    input_p, input_f = rename_path_sub_ses(bids, sub, ses, input_path)
    ref_p, ref_f = rename_path_sub_ses(bids, sub, ses, ref_path)
    
    reg_space = ''
    if not reg_name:
        ref_d = ref_f.split('.')[0].split('_')
        reg_space = f'reg-{ref_d[-1]}'
        input_d = input_f.split('.')[0].split('_')
        input_d.insert(-1, reg_space)
        out_name = '_'.join(input_d)
    
    else:
        reg_name_d = reg_name.split('_')
        for e in reg_name_d:
            if 'reg-' in e:
                reg_space = e
        out_name = reg_name
        
    if not deriv:
        deriv = f'registrations/{reg_space}'
    
    sub_ses_deriv = pjoin(bids, 'derivatives', deriv, f'sub-{sub}', f'ses-{ses}')
        
    return pjoin(sub_ses_deriv, out_name)


def is_subpath(main_path, sub_path):
    main_path = os.path.abspath(main_path)
    sub_path = os.path.abspath(sub_path)
    try:
        common_path = os.path.commonpath([main_path, sub_path])
        return common_path == sub_path
    except ValueError:
        return False


def get_session_list(bids, subj, ses_details, check_if_exist=True):
    """Helper function to get the list of sessions for a given subject."""
    sess = []
    if ses_details == 'all':
        for d in os.listdir(pjoin(bids, f'sub-{subj}')):
            if d.startswith('ses-'):
                sess.append(d.split('-')[1])
    else:
        for s in ses_details.split(','):
            if '-' in s:
                s0, s1 = map(int, s.split('-'))
                for si in range(s0, s1 + 1):
                    si_str = str(si).zfill(2)
                    if check_if_exist:
                        if os.path.isdir(pjoin(bids, f'sub-{subj}', f'ses-{si_str}')):
                            sess.append(si_str)
                    else:
                        sess.append(si_str)
            else:
                if check_if_exist:
                    if os.path.isdir(pjoin(bids, f'sub-{subj}', f'ses-{s}')):
                        sess.append(s)
                else:
                    sess.append(s)
    return sess

def process_subject_range(bids, sub_range, ses_details, check_if_exist=True):
    """Helper function to process a range of subjects."""
    subjects_and_sessions = []
    sub0, sub1 = map(int, sub_range.split('-'))
    for subi in range(sub0, sub1 + 1):
        subi_str = str(subi).zfill(3)
        if not os.path.isdir(pjoin(bids, f'sub-{subi_str}')) and check_if_exist:
            continue
        sess = get_session_list(bids, subi_str, ses_details, check_if_exist=check_if_exist)
        subjects_and_sessions.append((subi_str, sess))
    return subjects_and_sessions

def find_subjects_and_sessions(bids, sub, ses, check_if_exist=True):
    subjects_and_sessions = []

    if sub == 'all':
        # Process all subjects
        for dirs in os.listdir(bids):
            if dirs.startswith('sub-'):
                subj = dirs.split('-')[1]
                sess = get_session_list(bids, subj, ses)
                subjects_and_sessions.append((subj, sess))
    else:
        # Process specified subjects
        for sub_item in sub.split(','):
            if '-' in sub_item:
                subjects_and_sessions.extend(process_subject_range(bids, sub_item, ses, check_if_exist=check_if_exist))
            else:
                if not os.path.isdir(pjoin(bids, f'sub-{sub_item}')) and check_if_exist:
                    continue
                sess = get_session_list(bids, sub_item, ses, check_if_exist=check_if_exist)
                subjects_and_sessions.append((sub_item, sess))
    
    return sorted(subjects_and_sessions)
    


if __name__ == '__main__':
    
    description = '''
bids_registration:
    perform registration or apply transformation matrix using ANTs
    '''
    
    usage = '\npython %(prog)s bids sub ses [OPTIONS]'
    
    parser = argparse.ArgumentParser(description=description, usage=usage)
    
    parser.add_argument('bids', type=str, help='path towards a bids formatted database')
    parser.add_argument('sub', type=str, help='sub ID or list of sub ID to process (e.g. 001,002). The keyword "all" will select all subjects of the database, while "-" allow to select subject ID in between two border (e.g. 001-010)')
    parser.add_argument('ses', type=str, help='ses ID or list of ses ID to process (e.g. 01,02). The keyword "all" will select all sessions of the database, while "-" allow to select session ID in between two border (e.g. 01-10)')
    parser.add_argument('--input-image', '-i', dest='input', type=str, help='reference path of input image to register', required=True)
    parser.add_argument('--reference-image', '-r', dest='ref', type=str, help='reference path of reference image for the registration', required=True)
    parser.add_argument('--quick', dest='quick', help='use the quick version of antsRegistrationSyN (default=False)', action='store_const', const=True, default=False, required=False)
    parser.add_argument('--apply-transform', dest='transform', help='apply transform instead of doing a registration', action='store_const', const=True, default=False, required=False)
    parser.add_argument('--transformation-matrix', '-t', dest='trans_mat', type=str, help='reference path of transformation matrix to apply to input image (used when --apply-transform option is used)', required=False)
    parser.add_argument('--label', dest='label', help='use if the input image is a label image (default=False)', action='store_const', const=True, default=False, required=False)
    parser.add_argument('--inverse', dest='inverse', help='apply inverse transformation matrix (default=False)', action='store_const', const=True, default=False, required=False)
    parser.add_argument('--derivative', '-d', dest='deriv', type=str, help='derivative folder name to store the output (default: registrations/reg-{space of reference image})', default=None, required=False)
    parser.add_argument('--reg-name', '-ro', dest='reg_name', type=str, help='name of the output sequence name (default: add reg-{space of reference image} to input img name', default=None, required=False)
    parser.add_argument('--use-docker', dest='use_docker', help='use docker version of ANTs instead of local one (default=False)', action='store_const', const=True, default=False, required=False)
    
    # Parse the arguments
    try:
        args = parser.parse_args()
    except SystemExit as e:
        # This block catches the SystemExit exception raised by argparse when required args are missing
        if e.code != 0:  # Non-zero code indicates an error
            parser.print_help()
        sys.exit(e.code)
        
    bids = args.bids
    
    subjects_and_sessions = find_subjects_and_sessions(bids, args.sub, args.ses)
    
    for sub, sess in subjects_and_sessions:
        for ses in sess:
            print(sub, ses)
            
            if args.use_docker:
                if args.transform:
                    bids_apply_transforms_docker(bids, sub, ses, args.input, args.ref, args.trans_mat, deriv=args.deriv, reg_name=args.reg_name, label=args.label, inverse=args.inverse)
                else:
                    bids_registration_docker(bids, sub, ses, args.input, args.ref, deriv=args.deriv, out_name=args.reg_name, quick=args.quick)
            else:
                if args.transform:
                    bids_apply_transforms(bids, sub, ses, args.input, args.ref, args.trans_mat, deriv=args.deriv, reg_name=args.reg_name, label=args.label, inverse=args.inverse)
                else:
                    bids_registration(bids, sub, ses, args.input, args.ref, deriv=args.deriv, reg_name=args.reg_name, quick=args.quick)
    
    