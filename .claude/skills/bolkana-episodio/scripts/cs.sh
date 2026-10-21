#!/bin/bash
# cs.sh '<comando>' — ejecuta un comando en el Codespace del podcast (cwd = raíz del repo)
export PATH=~/.local/bin:$PATH
exec gh codespace ssh -c musical-broccoli-vg76w7vqw79f7gp -- "cd /workspaces/bolkana-podcast && $1"
