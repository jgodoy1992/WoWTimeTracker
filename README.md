Small idea I had while reading about automation projects in Python: I like to play some WoW on my spare time, but I usually lose track of time, so I thought "Why not have a small script that tracks the amount of time per session I spend logged into WoW, and notifes by email the time elapsed?"
Now, the thing is "why not also create a xlsx or csv file so that I can therefore visualie this data and better manage my free time?". And so, this is how this idea was born

  Things I learned:
  - Use of the yagmail (yet another gmail) library to send email to user
  - Use of watchdog library to monitor file systems events
  - Use of pandas to write data frame to xlsx or csv file for later analyses
