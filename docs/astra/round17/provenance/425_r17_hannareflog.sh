# Read-only: did the HANNA checkout ever move after cloning?
cd "$HOME/Projects/BIP Free Predictive Modeling/third_party/HANNA" || exit 1
git reflog --date=iso | head -10
stat -f '%Sm %N' -t '%Y-%m-%d %H:%M' .git models/HANNA/ensemble/HANNA_parameters_binary0.pt
