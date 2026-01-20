github_release() {
	ORIGINAL_DIR=$(pwd)
	echo "[*] Preparing clean release…"

	rm -rf /tmp/ldh_release
	mkdir -p /tmp/ldh_release/LazyDeveloperHelper

	echo "[*] Copying required files:"

	cp -r lua/LazyDeveloperHelper/commands/ /tmp/ldh_release/LazyDeveloperHelper/
	cp -r lua/LazyDeveloperHelper/init.lua /tmp/ldh_release/LazyDeveloperHelper/
	cp -r lua/LazyDeveloperHelper/python /tmp/ldh_release/LazyDeveloperHelper/
	cp -r plugin/ /tmp/ldh_release/LazyDeveloperHelper/
	cp -r CHANGELOG.md /tmp/ldh_release/LazyDeveloperHelper/

	echo "[*] Copying files for test workability"
	cp -r test_files/test.* /tmp/ldh_release/LazyDeveloperHelper/

	echo "[*] Copying README.md, LICENSE files"
	cp README.md /tmp/ldh_release/LazyDeveloperHelper/
	cp LICENSE /tmp/ldh_release/LazyDeveloperHelper/

	echo "[*] Zipping to /tmp/ldh_release:"
	cd /tmp/ldh_release
	zip -r LazyDeveloperHelper.zip LazyDeveloperHelper >/dev/null

	echo "[*] Moving archive to original dist:"
	mkdir -p "$ORIGINAL_DIR/dist"
	mv LazyDeveloperHelper.zip "$ORIGINAL_DIR/dist/"

	echo "[✓] Done. Clean .zip is in dist/, size:"
	du -h "$ORIGINAL_DIR/dist/LazyDeveloperHelper.zip"

	cd "$ORIGINAL_DIR"
}
