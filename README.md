# Buildozer action

Build your Python/[Kivy](https://github.com/kivy/kivy) applications for Android
with [Buildozer](https://github.com/kivy/buildozer). This action uses official
Buildozer [Docker image](https://github.com/kivy/buildozer/blob/master/Dockerfile),
but adds some features and patches to use in GitHub Actions.

## Example usage

```yaml
- name: Build with Buildozer
  uses: ArtemSBulgakov/buildozer-action@v1
```

## License

ArtemSBulgakov/buildozer-action is released under the terms of the
[MIT License](LICENSE).
