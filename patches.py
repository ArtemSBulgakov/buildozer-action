import os
import buildozer

print("Changing global_buildozer_dir")
source = open(buildozer.__file__, "r", encoding="utf-8").read()
new_source = source.replace(
    """
    @property
    def global_buildozer_dir(self):
        return join(expanduser('~'), '.buildozer')
""",
    f"""
    @property
    def global_buildozer_dir(self):
        return '{os.environ["GITHUB_WORKSPACE"]}/.buildozer_global'
""",
)
if new_source == source:
    print("::warning::Cannot change global buildozer directory. Update buildozer-action to new version or create a Bug Request")
open(buildozer.__file__, "w", encoding="utf-8").write(new_source)
