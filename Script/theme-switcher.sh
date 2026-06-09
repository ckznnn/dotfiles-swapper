#!/bin/bash

echo ""
echo "  Script Launcher"
echo "  ---------------"
echo "  1) Gruvbox Dark"
echo "  2) Gruvbox Light"
echo "  3) Everforest Dark"
echo "  4) Tokyo Night"
echo ""
read -rp "  Enter a number [1-4]: " choice

case "$choice" in
    1) bash ~/dotfiles-swapper/Script/gruvbox-dark.sh ;;
    2) bash ~/dotfiles-swapper/Script/gruvbox-light.sh ;;
    3) bash ~/dotfiles-swapper/Script/everforest-dark.sh ;;
    4) bash ~/dotfiles-swapper/Script/tokyonight.sh ;;
    *)
        echo "  Invalid choice: $choice"
        exit 1
        ;;
esac
