# Read-only: HANNA weight files and tree cleanliness.
H="$HOME/Projects/BIP Free Predictive Modeling/third_party/HANNA"; cd "$H" || exit 1
git status --porcelain | head -5; echo "dirty_lines=$(git status --porcelain | wc -l)"
find models -type f | sort | head -80 | while read f; do shasum -a 256 "$f"; done
echo "nfiles=$(find models -type f | wc -l)"
find models -type f | sort | xargs shasum -a 256 | shasum -a 256 | sed 's/^/aggregate /'
