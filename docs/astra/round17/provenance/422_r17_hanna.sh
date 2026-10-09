# Read-only: HANNA source identity.
H="$HOME/Projects/BIP Free Predictive Modeling/third_party/HANNA"; cd "$H" || exit 1
git log -1 --format='%H %ad %s' 2>/dev/null; git remote -v 2>/dev/null | head -2
ls; find . -maxdepth 3 \( -name "*.pt" -o -name "*.pth" -o -name "*.ckpt" \) | head -15 | while read f; do shasum -a 256 "$f"; done
