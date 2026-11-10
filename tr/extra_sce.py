# Messages patcher.find_messages() misses (text op 78 whose text starts with a half-width character, e.g. a digit).
# {entry: [(offset of the 78 op in the entry, original Japanese for reference, English), ...]}
# build.py appends them after the found messages, so the e###.py message indexes don't shift.
# Found by tools/jpleft.py (whole-disc scan for untouched Japanese).
X = {
242: [(0xb67, '2人でそうじをしました。／部屋の中はピカピカです。',
       "Cleaned up together.\nThe room is sparkling！")],   # Lettuce's room, after Ichigo offers to help clean
}
