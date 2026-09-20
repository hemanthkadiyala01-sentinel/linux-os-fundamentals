# Linux File Permissions Investigation

## Objective
Investigate Linux file permissions, ownership, umask, and user-based access control.

## Tools Used
- ls -l
- stat
- chmod
- umask
- id
- sudo

## Investigation Findings

### 1. File Permission Configuration
- private.txt: 600
- public.txt: 644 initially, changed to 640
- script.sh: 755

### 2. Default umask
- umask: 0022
- New files: 644
- New directories: 755

### 3. Permission Modification
Changed public.txt from 644 to 640 using chmod.

### 4. Access Control Testing
- User bunny successfully read public.txt.
- User nobody received Permission denied when accessing private.txt and public.txt.
- nobody belongs to nogroup and is not a member of the bunny group.

## Security Relevance
File permissions help protect sensitive information and restrict unauthorized access. Security analysts should inspect ownership, permissions, groups, and access failures during investigations.

## Conclusion
The investigation demonstrated Linux permission notation, numeric modes, umask behavior, chmod, ownership, group membership, and user-based access control.
