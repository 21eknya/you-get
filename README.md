This is a forked project to add an additional translated caption track for youtube videos.

-T <language code> is added. Only zh-hans is supported for now.

All credit goes to https://github.com/soimort/you-get .

Simple usage:

you-get -o <dir to save> -T zh-hans <url of the video> # Download video to specific dir. Add a translated (in zh-hans) caption track in srt file.

you-get <url of the video> -i # Inspect supported formats.

you-get -o <dir to save> -T zh <url of the video> --itag <code> # Download video like the 1 but in specific format.
