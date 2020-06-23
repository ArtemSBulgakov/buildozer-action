# Buildozer action

Build your Python/[Kivy](https://github.com/kivy/kivy) applications for Android
with [Buildozer](https://github.com/kivy/buildozer). This action uses official
Buildozer [Docker image](https://github.com/kivy/buildozer/blob/master/Dockerfile),
but adds some features and patches to use in GitHub Actions.

## Inputs

### `command`

**Required** Command to start Buildozer.

- _Default:_ `buildozer android debug` _(iOS and OSX is not supported because Docker cannot run on MacOS)_.
- For more commands use `;` as delimiter: `python3 setup.py build_ext --inplace; buildozer android debug`.

### `workdir`

**Required** Working directory where buildozer.spec is located.

- _Default:_ `.` (top directory).
- Set to `src` if buildozer.spec is in `src` directory.

## Example usage

```yaml
- name: Build with Buildozer
  uses: ArtemSBulgakov/buildozer-action@v1
  with:
    command: buildozer android debug
    workir: src
```

## License

ArtemSBulgakov/buildozer-action is released under the terms of the
[MIT License](LICENSE).
