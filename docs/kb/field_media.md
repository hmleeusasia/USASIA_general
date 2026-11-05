# Field photos and attachments (D-20261105-9)
Photos, screenshots and files the user sends in chat are stored in Google Drive and linked from the repo with context. The repo never holds the image.

## Where (one place to change)
| Key | Value |
|---|---|
| Root folder | `IT Field Photos` — https://drive.google.com/drive/folders/1mxg0zuzN2KZlexA4gMdPkQpdK6XSCg2U (hmlee My Drive, private) |
| Layout | `<root>/<YYYY>/<YYYY-MM-DD> <Store>/` |
| File name | `<YYYY-MM-DD>_<Store>_<topic>.<ext>` (self-describing; still makes sense after a move) |

Skills and logs read the root from this file only. When the folder moves, update this table once.

## Steps (each time media arrives)
1. Find or create the day/store folder under the root.
2. Upload. Cloud session: connector needs inline base64, so shrink first (crop, grayscale for screens, ~20 KB; text must stay readable). Full quality needed → the user uploads from the Drive app; Claude renames and links it.
3. In the day log entry (and the todo row's "다음", if any) add `Photo: <file name> — <Drive file link>`.
4. Sensitive content in the image (IPs, passwords, customer data) is fine in Drive; the repo text still leaves the values out (R-SEC-02).

## Moving to a shared drive later
- Moving a file or folder (My Drive → shared drive) keeps its file ID, so links in the repo keep working. Copying does not: always **move**, never copy + delete.
- Steps: move the whole `IT Field Photos` folder into the shared drive → update the root row above → note it in docs/drive-index. No log edits needed.
- Shared-drive members will see everything moved; check for anything personal before moving.
