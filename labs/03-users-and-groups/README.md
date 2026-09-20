# Lab 03: Users and Groups Investigation

## Objective
Investigate Linux users, groups, group membership, and group-based file permissions.

## Environment
- OS: Ubuntu on WSL
- User: bunny
- Project: Linux OS Fundamentals

## Investigation Results

### 1. Current User
- Username: bunny
- UID: 1000
- Primary Group: bunny
- GID: 1000

### 2. Security Group
- Group Name: securitylab
- Group ID: 1002
- Member: bunny

### 3. File Permissions
- File: group-file.txt
- Owner: bunny
- Group: securitylab
- Permissions: 640

Permission breakdown:
- Owner: read and write
- Group: read
- Others: no permissions

### 4. Access Control Test
The bunny user successfully read the file.

The nobody user received Permission denied because it belongs to nogroup and is not a member of securitylab.

### 5. Key Learning
Linux group ownership and permission bits control access to files. Users who are not the owner or members of the assigned group may be denied access.
