FROM kivy/buildozer:latest
# See https://github.com/kivy/buildozer/blob/master/Dockerfile

COPY entrypoint.sh /action/entrypoint.sh

ENTRYPOINT ["/action/entrypoint.sh"]
