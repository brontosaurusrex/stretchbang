alias lst='ls -clhtr'
alias up='sudo apt-get update && sudo apt-get dist-upgrade -y'
alias mi='mediainfo'
alias htop='htop -C'
alias news='newsbeuter'
alias bcal='gcal -s Mon --cc-holidays=SI .'
alias 2017='gcal --cc-holidays=SI -s Mon -n 2017'
alias search='apt-cache search'
alias nvim='nvim -c "colors molokai"'
alias docx='unoconv -f text --stdout'
alias weather="wget wttr.in 2>/dev/null -O - | grep -v 'New feature*\|Follow'"
alias today='wget wttr.in/?0Q 2>/dev/null -O -'
alias inform='curl -e "No Cookies Please, Do not track and spy. Do not inform me about my ad blocker. Go home and rethink your life."  -A "User"'
alias space='gdmap -f . &'
alias ans='cat ~/.pans.txt'
alias asciize='img2txt -W "$( tput cols )" -f utf8 -d random'
alias space='gdmap -f . &'
alias rndPlay='mpv --no-config --no-video --no-resume-playback --no-ytdl --af=lavfi=[loudnorm=LRA=10:I=-17] --shuffle *'
