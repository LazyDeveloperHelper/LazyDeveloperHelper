vim_org_release() {
	echo "[*] Preparing clean release…"

	rm -f dist/LazyDeveloperHelper.zip
	rm -rf /tmp/ldh_release

	echo "[*] Copying folders"
	mkdir -p /tmp/ldh_release/LazyDeveloperHelper
	cp -r lua/LazyDeveloperHelper/ /tmp/ldh_release/LazyDeveloperHelper/

	echo "[*] Copying License, changelog.md"
	cp LICENSE CHANGELOG.md /tmp/ldh_release/LazyDeveloperHelper/

	echo "[*] Zipping..."
	cd /tmp/ldh_release
	zip -r LazyDeveloperHelper.zip LazyDeveloperHelper >/dev/null

	echo "[*] Moving..."
	mkdir -p ~/Projects/LazyDeveloperHelper/dist
	mv LazyDeveloperHelper.zip ~/Projects/LazyDeveloperHelper/dist/

	echo "[✓] Done. Clean .zip is in dist/, size:"
	du -h ~/Projects/LazyDeveloperHelper/dist/LazyDeveloperHelper.zip
}
