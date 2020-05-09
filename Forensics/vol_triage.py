#!/bin/bash
# Update global variables per your systems configuration.
# How to run ./vol_triage.py linux
VOL="./Tools/volatility/vol.py" # Specify path to vol.py
MEM_DUMP="/home/dllcoolj/CTF/Sharky/MemoryDump/dump.mem"  # Specify the memory dump path
MEM_PROFILE="LinuxCentos77ax64" # Specify memory profile (run vol --info to see which ones you have.)

# Windows memory triage commands
WINDOWS_CMDS=(
    imageinfo
    pslist
    getsids
    pstree
    psscan
    dllist
    handles
    cmdscan
    netscan
    connections
)

# Linux memory triage commands
LINUX_CMDS=( 
    linux_pslist 
    linux_psaux
    linux_pstree
    linux_pslist_cache
    linux_pidhashtable
    linux_psxview
    linux_lsof
    linux_find_file
    linux_bash
    linux_lsmod
    linux_dmesg
    linux_arp
    linux_ifconfig
    linux_netstat
)

# Run Linux triage commands and tar up .txt output for delivery
linux_triage() {
    for cmd in ${LINUX_CMDS[@]}; do 
        echo -e "[$(date -Is)] Runing $cmd"
        if [[ "$cmd" == "linux_find_file" ]]; then
            $VOL -f $MEM_DUMP --profile=$MEM_PROFILE $cmd -L > "$MEM_PROFILE-$cmd.txt"
        fi
            $VOL -f $MEM_DUMP --profile=$MEM_PROFILE $cmd > "$MEM_PROFILE-$cmd.txt"
    done
}

# Run Windows triage and tar up .txt output for delievery
windows_triage() {
    for cmd in ${WINDOWS_CMDS[@]}; do 
        echo -e "[$(date -Is)] Runing $cmd"
        $VOL -f $MEM_DUMP --profile=$MEM_PROFILE $cmd > "$MEM_PROFILE-$cmd.txt"
    done
}


# Tar up .txt files
wrap_up() {
    tar czvf "$MEM_PROFILE-VOL.tar.gz" *.txt;

    if [[ $? -eq 0 ]]; then
        echo -e "[+] Successfully tar'd, now distribute to the team and get those flags!";
    else
        echo -e "[!] Something went horribly wrong!";
    fi
}

# Main
if [[ "$1" == "linux" ]]; then
    linux_triage;
elif [[ "$1" == "windows" ]]; then
    windows_triage
else
    echo -e "[!] Unknown OS, please specify linux or windows";
    exit 1;
fi

wrap_up;
