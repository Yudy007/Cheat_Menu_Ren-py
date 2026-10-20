# -*- coding: utf-8 -*-
# ==============================================================================
# CHEAT MENU CLOUD CONNECTOR FOR REN'PY (GITHUB CLOUD EDITION)
# ==============================================================================
# Kho lưu trữ chính thức: https://github.com/Yudy007/Cheat_Menu_Ren-py
# Tác giả: Yudy007
# Tương thích hoàn hảo: Ren'Py 6, Ren'Py 7 (Python 2.7) & Ren'Py 8, 9 (Python 3.x)
# ==============================================================================
# ĐẶC ĐIỂM:
# 1. 100% ĐÁM MÂY GITHUB: Hoàn toàn không phụ thuộc vào bất kỳ đường dẫn ổ đĩa
#    cố định nào trên máy. Kết nối trực tiếp đến GitHub Yudy007 qua Internet.
# 2. CHẠY NGAY TỪ LẦN MỞ ĐẦU TIÊN (Dynamic Script Injection):
#    Tự động tải cheat_menu.rpy từ GitHub về game và nạp thẳng vào Ren'Py
#    ngay trong vòng lặp load_script ban đầu — KHÔNG CẦN KHỞI ĐỘNG LẠI 2 LẦN.
# 3. TỰ ĐỘNG SỬA FILE LẬP TỨC:
#    - Tự động khôi phục cheat_menu.rpy sạch từ GitHub nếu file bị lỗi hoặc hỏng.
#    - Tự động dọn sạch cache bytecode (.rpyc) xung đột.
#    - Tự động vá lỗi thiếu biến (NameError) và ghi file 00_cheat_autofix.rpy.
#    - Tự động vá lỗi thiếu hàm / thuộc tính (AttributeError).
# 4. TỰ ĐỘNG ĐỒNG BỘ & ĐẨY BẢN SỬA LỖI LÊN GITHUB (GITHUB REST API):
#    - Tự động đồng bộ bản sửa lỗi lên GitHub khi có token trong github_token.txt.
#    - Đẩy thủ công bất kỳ lúc nào qua phím tắt hoặc nút bấm trong Bảng Cứu Hộ.
# 5. PHÍM TẮT:
#    - Shift + F11: Tải bản mới nhất từ GitHub & Tự sửa lỗi ngay lập tức.
#    - Shift + F10: Xóa sạch cache bytecode .rpyc và khởi động lại sạch sẽ.
#    - Ctrl + Shift + F12: Đẩy bản sửa lỗi cheat_menu.rpy trực tiếp lên GitHub qua API.
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. GIAI ĐOẠN KHỞI ĐỘNG SỚM (PYTHON EARLY: KẾT NỐI GITHUB & NẠP ĐỘNG)
# ------------------------------------------------------------------------------
python early:
    import os
    import sys
    import shutil
    import time

    try:
        _cheat_conn_unicode = unicode
    except NameError:
        _cheat_conn_unicode = str

    def _cheat_conn_log(msg):
        try:
            if hasattr(renpy, 'log'):
                renpy.log("[CheatConnector] " + str(msg))
        except Exception:
            pass

    # 1.1 Xác định chính xác thư mục game hiện tại
    def _cheat_conn_get_gamedir():
        try:
            if hasattr(renpy, 'config') and getattr(renpy.config, 'gamedir', None):
                return os.path.abspath(renpy.config.gamedir)
        except Exception:
            pass
        try:
            curr_dir = os.path.dirname(os.path.abspath(__file__))
            if os.path.basename(curr_dir).lower() == 'game':
                return curr_dir
            if os.path.isdir(os.path.join(curr_dir, 'game')):
                return os.path.join(curr_dir, 'game')
            return curr_dir
        except Exception:
            pass
        if os.path.isdir('game'):
            return os.path.abspath('game')
        return os.path.abspath('.')

    # --------------------------------------------------------------------------
    # 1.2 CẤU HÌNH LIÊN KẾT GITHUB CHÍNH THỨC (KHÔNG DÙNG ĐƯỜNG DẪN Ổ ĐĨA CỤC BỘ)
    # --------------------------------------------------------------------------
    _cheat_conn_github_menu_url = "https://raw.githubusercontent.com/Yudy007/Cheat_Menu_Ren-py/main/cheat_menu.rpy"
    _cheat_conn_github_conn_url = "https://raw.githubusercontent.com/Yudy007/Cheat_Menu_Ren-py/main/cheat_connect.rpy"

    # Hàm tải file từ GitHub an toàn tuyệt đối qua mạng
    def _cheat_conn_download_from_github(url, dest_path):
        if not url:
            return False
        # Cách 1: Dùng os.system với curl.exe (Tương thích 100% mọi bản Python 2 & 3 trên Windows)
        try:
            cmd = 'curl.exe -s -L "%s" -o "%s"' % (url, dest_path)
            ret = os.system(cmd)
            if ret == 0 and os.path.isfile(dest_path) and os.path.getsize(dest_path) > 1000:
                return True
        except Exception:
            pass
        # Cách 2: Dùng subprocess với curl.exe
        try:
            import subprocess
            cmd = ['curl.exe', '-s', '-L', url, '-o', dest_path]
            ret = subprocess.call(cmd)
            if ret == 0 and os.path.isfile(dest_path) and os.path.getsize(dest_path) > 1000:
                return True
        except Exception:
            pass
        # Cách 3: Dùng urllib của Python (Ren'Py 8/Python 3)
        try:
            import urllib.request as urllib_req
            req = urllib_req.Request(url, headers={'User-Agent': 'RenPy-Cheat-Connector'})
            resp = urllib_req.urlopen(req, timeout=10)
            content = resp.read()
            if len(content) > 1000:
                with open(dest_path, 'wb') as f:
                    f.write(content)
                return True
        except Exception:
            pass
        return False

    # Biến trạng thái toàn cục cho phiên khởi động
    _cheat_conn_gamedir = _cheat_conn_get_gamedir()
    _cheat_conn_target_file = os.path.join(_cheat_conn_gamedir, "cheat_menu.rpy")
    _cheat_conn_target_rpyc = os.path.join(_cheat_conn_gamedir, "cheat_menu.rpyc")
    _cheat_conn_updated_now = False

    # 1.3 Cơ chế Nạp Động Cốt Lõi (Dynamic Script Injection):
    # Đưa cheat_menu vào thẳng danh sách quét của load_script() ngay trong vòng lặp hiện tại!
    def _cheat_conn_inject_into_renpy_script(gamedir):
        try:
            if hasattr(renpy, 'loader') and hasattr(renpy.loader, 'cleardirfiles'):
                renpy.loader.cleardirfiles()

            target_tuple = ('cheat_menu', gamedir)
            injected = False

            if hasattr(renpy, 'game') and hasattr(renpy.game, 'script'):
                s = renpy.game.script
                for attr in ('script_files', 'game_script_files'):
                    if hasattr(s, attr):
                        flist = getattr(s, attr)
                        if isinstance(flist, list):
                            if not any(item[0] == 'cheat_menu' for item in flist):
                                flist.append(target_tuple)
                                injected = True

            f = sys._getframe(1)
            while f:
                f_locals = f.f_locals
                if 'script_files' in f_locals and isinstance(f_locals['script_files'], list):
                    sf = f_locals['script_files']
                    if not any(item[0] == 'cheat_menu' for item in sf):
                        sf.append(target_tuple)
                        injected = True
                if 'self' in f_locals:
                    obj = f_locals['self']
                    if hasattr(obj, 'script_files') and isinstance(obj.script_files, list):
                        if not any(item[0] == 'cheat_menu' for item in obj.script_files):
                            obj.script_files.append(target_tuple)
                            injected = True
                f = f.f_back

            if injected:
                _cheat_conn_log("Successfully injected cheat_menu into active load_script queue.")
            return injected
        except Exception as _inj_err:
            _cheat_conn_log("Injection error: " + str(_inj_err))
            return False

    # 1.4 Kiểm tra sự hiện diện của cheat_menu.rpy trong game:
    # Nếu CHƯA CÓ hoặc BỊ HỎNG (size < 1000 bytes) -> Tải trực tiếp từ GitHub ngay lập tức!
    try:
        need_download = False
        if not os.path.isfile(_cheat_conn_target_file):
            need_download = True
        elif os.path.getsize(_cheat_conn_target_file) < 1000:
            need_download = True

        if need_download:
            _cheat_conn_log("cheat_menu.rpy not found or corrupted. Downloading from GitHub...")
            if _cheat_conn_download_from_github(_cheat_conn_github_menu_url, _cheat_conn_target_file):
                if os.path.isfile(_cheat_conn_target_rpyc):
                    try:
                        os.remove(_cheat_conn_target_rpyc)
                    except Exception:
                        pass
                _cheat_conn_updated_now = True
                _cheat_conn_log("Downloaded cheat_menu.rpy from GitHub successfully.")
                # Nạp động ngay trong lần khởi động này
                _cheat_conn_inject_into_renpy_script(_cheat_conn_gamedir)

        # 1.5 Dọn dẹp cache .rpyc cũ nếu phát hiện file nguồn .rpy mới hơn
        if os.path.isfile(_cheat_conn_target_file) and os.path.isfile(_cheat_conn_target_rpyc):
            try:
                if os.path.getmtime(_cheat_conn_target_file) > os.path.getmtime(_cheat_conn_target_rpyc):
                    os.remove(_cheat_conn_target_rpyc)
                    _cheat_conn_log("Removed stale cheat_menu.rpyc.")
            except Exception:
                pass
    except Exception as _early_err:
        _cheat_conn_log("Early init error: " + str(_early_err))


# ------------------------------------------------------------------------------
# 2. KHỞI TẠO CẤP CAO & VÁ LỖI TƯƠNG THÍCH MỌI PHIÊN BẢN (POLYFILL ENGINE)
# ------------------------------------------------------------------------------
init -1999 python:
    # 2.1 Polyfill các hàm thuần khiết decorator chuẩn của Ren'Py
    def _cheat_conn_noop_decorator(*args, **kwargs):
        if not args:
            return lambda fn: fn
        return args[0]

    for _fn_name in ('pure', 'const', 'not_const'):
        if not hasattr(renpy, _fn_name):
            setattr(renpy, _fn_name, _cheat_conn_noop_decorator)
        if hasattr(renpy, 'python') and not hasattr(renpy.python, _fn_name):
            setattr(renpy.python, _fn_name, _cheat_conn_noop_decorator)

    # 2.2 Bọc hàm renpy.notify an toàn tuyệt đối
    try:
        import renpy.exports as _renpy_exports
        _real_notify = getattr(_renpy_exports, 'notify', None)
        if _real_notify is not None and not getattr(_real_notify, '_cheat_conn_wrapped', False):
            def _cheat_conn_safe_notify(msg, *args, **kwargs):
                try:
                    if hasattr(renpy, 'game') and hasattr(renpy.game, 'context'):
                        ctx = renpy.game.context()
                        if getattr(ctx, 'init_phase', False):
                            return None
                except Exception:
                    pass
                try:
                    return _real_notify(msg, *args, **kwargs)
                except Exception:
                    return None
            _cheat_conn_safe_notify._cheat_conn_wrapped = True
            renpy.notify = _cheat_conn_safe_notify
            if hasattr(renpy, 'exports'):
                renpy.exports.notify = _cheat_conn_safe_notify
    except Exception:
        pass

    # 2.3 Biến lưu trữ trạng thái phục hồi lỗi toàn cục
    renpy.store._cheat_conn_last_error = None
    renpy.store._cheat_conn_error_time = 0
    renpy.store._cheat_conn_error_count = 0


# ------------------------------------------------------------------------------
# 3. HỆ THỐNG QUẢN LÝ NẠP LẠI & HOT-RELOAD TỰ ĐỘNG
# ------------------------------------------------------------------------------
init -99 python:
    def _cheat_conn_notify(msg):
        try:
            if hasattr(renpy, 'notify') and callable(renpy.notify):
                renpy.notify(msg)
        except Exception:
            pass

    # Hàm khởi động lại sạch sẽ toàn bộ môi trường Ren'Py
    def cheat_conn_clean_restart():
        try:
            if hasattr(renpy, 'utter_restart'):
                renpy.utter_restart()
            elif hasattr(renpy, 'reload_script'):
                renpy.reload_script()
            else:
                renpy.quit(relaunch=True)
        except (Exception, BaseException) as e:
            ex_name = e.__class__.__name__
            if 'Restart' in ex_name or 'Reload' in ex_name or 'Quit' in ex_name:
                raise


# ------------------------------------------------------------------------------
# 4. BỘ CỨU HỘ VÀ SỬA LỖI TỨC THÌ (GITHUB CLOUD AUTO-REPAIR ENGINE)
# ------------------------------------------------------------------------------
init -50 python:
    # 4.1 Hàm tải bản mới nhất từ GitHub và tự động sửa mọi lỗi (Shift + F11)
    def cheat_connect_force_update():
        """
        Nút bấm và Phím tắt: Ép buộc tải lại bản mới nhất trực tiếp từ GitHub,
        xóa sạch bytecode .rpyc, sửa lỗi dữ liệu persistent và khởi động lại game.
        """
        try:
            _cheat_conn_notify("🌐 Đang kết nối tới GitHub Yudy007 để tải bản mới...")
            gdir = _cheat_conn_get_gamedir()
            target = os.path.join(gdir, "cheat_menu.rpy")
            target_rpyc = os.path.join(gdir, "cheat_menu.rpyc")
            temp_target = target + ".download"

            # Tải về file tạm trước để đảm bảo tải trọn vẹn
            if _cheat_conn_download_from_github(_cheat_conn_github_menu_url, temp_target):
                if os.path.isfile(target):
                    try:
                        shutil.copy2(target, target + ".bak")
                    except Exception:
                        pass
                shutil.move(temp_target, target)

                if os.path.isfile(target_rpyc):
                    try:
                        os.remove(target_rpyc)
                    except Exception:
                        pass

                for c_name in ("00_cheat_connect.rpyc", "cheat_connect.rpyc"):
                    c_path = os.path.join(gdir, c_name)
                    if os.path.isfile(c_path):
                        try:
                            os.remove(c_path)
                        except Exception:
                            pass

                # Khắc phục dữ liệu persistent nếu có
                try:
                    if hasattr(renpy, 'persistent'):
                        if not hasattr(persistent, 'cm_bar_visible'):
                            persistent.cm_bar_visible = True
                        if not hasattr(persistent, 'cm_single_key_shortcuts'):
                            persistent.cm_single_key_shortcuts = True
                except Exception:
                    pass

                _cheat_conn_notify("⚡ [GitHub Cloud] Cập nhật từ GitHub thành công! Đang nạp lại...")
                renpy.store._cheat_conn_last_error = None
                cheat_conn_clean_restart()
            else:
                _cheat_conn_notify("⚠️ Không thể tải từ GitHub! Vui lòng kiểm tra kết nối mạng.")
        except (Exception, BaseException) as e:
            ex_name = e.__class__.__name__
            if 'Restart' in ex_name or 'Reload' in ex_name:
                raise
            _cheat_conn_notify("Lỗi cập nhật: " + str(e))

    # 4.2 Hàm xóa sạch cache bytecode .rpyc và khởi động lại sạch sẽ (Shift + F10)
    def cheat_connect_clean_cache_and_restart():
        try:
            gdir = _cheat_conn_get_gamedir()
            count = 0
            for fname in os.listdir(gdir):
                if (fname.startswith("cheat_") or fname.startswith("00_cheat_")) and fname.endswith(".rpyc"):
                    try:
                        os.remove(os.path.join(gdir, fname))
                        count += 1
                    except Exception:
                        pass
            _cheat_conn_notify("🧹 Đã dọn sạch %d file cache bytecode! Đang khởi động lại..." % count)
            cheat_conn_clean_restart()
        except (Exception, BaseException) as e:
            ex_name = e.__class__.__name__
            if 'Restart' in ex_name or 'Reload' in ex_name:
                raise
            _cheat_conn_notify("Lỗi dọn cache: " + str(e))

    # 4.3 Mở trang GitHub chính thức của dự án trên trình duyệt
    def cheat_connect_open_github():
        try:
            import webbrowser
            webbrowser.open_new("https://github.com/Yudy007/Cheat_Menu_Ren-py")
        except Exception:
            _cheat_conn_notify("🌐 Link GitHub: https://github.com/Yudy007/Cheat_Menu_Ren-py")

    # --------------------------------------------------------------------------
    # 4.4 TỰ ĐỘNG ĐỒNG BỘ & ĐẨY BẢN SỬA LỖI LÊN GITHUB (GITHUB REST API)
    # --------------------------------------------------------------------------
    _cheat_conn_gh_owner = "Yudy007"
    _cheat_conn_gh_repo = "Cheat_Menu_Ren-py"
    _cheat_conn_gh_branch = "main"

    def _cheat_conn_get_github_token():
        for ev in ("GITHUB_TOKEN", "GH_TOKEN", "RENPY_GITHUB_TOKEN"):
            val = os.environ.get(ev, "").strip()
            if val:
                return val
        gdir = _cheat_conn_get_gamedir()
        candidates = [
            os.path.join(gdir, "github_token.txt"),
            os.path.join(os.path.dirname(gdir), "github_token.txt"),
            os.path.join(gdir, "token.txt"),
            os.path.join(os.path.expanduser("~"), ".renpy_github_token.txt"),
            os.path.join(os.path.expanduser("~"), "github_token.txt"),
        ]
        for c_path in candidates:
            try:
                if os.path.isfile(c_path):
                    with open(c_path, "r") as f:
                        for line in f:
                            line = line.strip().strip('"').strip("'")
                            if line and not line.startswith("#"):
                                return line
            except Exception:
                pass
        return None

    def _cheat_conn_ensure_token_template():
        gdir = _cheat_conn_get_gamedir()
        t_path = os.path.join(gdir, "github_token.txt")
        if not os.path.isfile(t_path):
            try:
                with open(t_path, "w") as f:
                    f.write("# ==========================================================\n")
                    f.write("# GITHUB PERSONAL ACCESS TOKEN (PAT) CHO CHEAT CONNECTOR\n")
                    f.write("# Kho luu tru: https://github.com/Yudy007/Cheat_Menu_Ren-py\n")
                    f.write("# ==========================================================\n")
                    f.write("# Huong dan:\n")
                    f.write("# 1. Truy cap: https://github.com/settings/tokens\n")
                    f.write("# 2. Tao token (Classic hoac Fine-grained) voi quyen: repo (hoac Contents: Read and Write)\n")
                    f.write("# 3. Dan ma token cua ban vao ngay dong duoi day va luu file:\n")
                    f.write("\n")
                    f.write("# ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
            except Exception:
                pass
        return t_path

    def _cheat_conn_push_single_file(filename, commit_msg=None):
        token = _cheat_conn_get_github_token()
        gdir = _cheat_conn_get_gamedir()
        filepath = os.path.join(gdir, filename)

        if not os.path.isfile(filepath):
            return False, "File khong ton tai tren may: " + str(filename)

        if not token:
            _cheat_conn_ensure_token_template()
            return False, "CHUA_CO_TOKEN"

        try:
            with open(filepath, "rb") as f:
                raw_bytes = f.read()
        except Exception as e:
            return False, "Loi doc file: " + str(e)

        if len(raw_bytes) < 10:
            return False, "File rong hoac qua nho."

        import base64
        import json
        import subprocess

        b64_content = base64.b64encode(raw_bytes)
        if not isinstance(b64_content, str):
            b64_content = b64_content.decode('ascii')

        api_url = "https://api.github.com/repos/%s/%s/contents/%s" % (
            _cheat_conn_gh_owner, _cheat_conn_gh_repo, filename
        )

        curr_sha = None
        try:
            get_cmd = [
                'curl.exe', '-s',
                '-H', 'Authorization: Bearer ' + token,
                '-H', 'Accept: application/vnd.github+json',
                '-H', 'User-Agent: RenPy-CheatConnect-Yudy007',
                api_url
            ]
            proc = subprocess.Popen(get_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
            if not isinstance(out, str):
                out = out.decode('utf-8', 'ignore')
            if out and '"sha"' in out:
                data = json.loads(out)
                if isinstance(data, dict) and 'sha' in data:
                    curr_sha = data['sha']
        except Exception:
            pass

        if not commit_msg:
            commit_msg = "Cap nhat sua loi %s tu Ren'Py Cheat Connector [skip ci]" % filename

        payload = {
            "message": commit_msg,
            "content": b64_content,
            "branch": _cheat_conn_gh_branch
        }
        if curr_sha:
            payload["sha"] = curr_sha

        temp_json = os.path.join(gdir, ".gh_upload_payload.json")
        try:
            payload_str = json.dumps(payload)
            try:
                payload_bytes = payload_str.encode('utf-8')
            except (UnicodeDecodeError, AttributeError):
                payload_bytes = payload_str

            with open(temp_json, "wb") as f:
                f.write(payload_bytes)

            put_cmd = [
                'curl.exe', '-s',
                '-X', 'PUT',
                '-H', 'Authorization: Bearer ' + token,
                '-H', 'Accept: application/vnd.github+json',
                '-H', 'User-Agent: RenPy-CheatConnect-Yudy007',
                '-d', '@' + temp_json,
                api_url
            ]
            proc = subprocess.Popen(put_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
            if not isinstance(out, str):
                out = out.decode('utf-8', 'ignore')

            if ('"commit"' in out or '"content"' in out) and ('"sha"' in out):
                return True, "Thanh cong"
            else:
                err_detail = "Loi khong xac dinh"
                try:
                    err_obj = json.loads(out)
                    if isinstance(err_obj, dict) and 'message' in err_obj:
                        err_detail = err_obj['message']
                except Exception:
                    err_detail = out[:120] if out else "Khong co phan hoi"
                return False, err_detail
        finally:
            if os.path.isfile(temp_json):
                try:
                    os.remove(temp_json)
                except Exception:
                    pass

    def cheat_connect_push_to_github(custom_msg=None):
        try:
            _cheat_conn_notify(u"🌐 Đang kết nối GitHub REST API để đẩy bản sửa lỗi...")
            token = _cheat_conn_get_github_token()
            if not token:
                _cheat_conn_ensure_token_template()
                _cheat_conn_notify(u"⚠️ Chưa có GitHub Token! Vui lòng dán token vào file 'github_token.txt'.")
                return False

            gdir = _cheat_conn_get_gamedir()
            success_count = 0
            err_reasons = []

            sync_targets = ["cheat_menu.rpy"]
            if os.path.isfile(os.path.join(gdir, "cheat_connect.rpy")):
                sync_targets.append("cheat_connect.rpy")
            elif os.path.isfile(os.path.join(gdir, "00_cheat_connect.rpy")):
                sync_targets.append("00_cheat_connect.rpy")

            for target_name in sync_targets:
                msg = custom_msg or (u"Cap nhat sua loi %s qua Ren'Py Cheat Connector [skip ci]" % target_name)
                ok, reason = _cheat_conn_push_single_file(target_name, msg)
                if ok:
                    success_count += 1
                else:
                    err_reasons.append("%s: %s" % (target_name, reason))

            if success_count > 0:
                _cheat_conn_notify(u"🚀 [GitHub API] Đã đẩy thành công %d file lên kho Yudy007/Cheat_Menu_Ren-py!" % success_count)
                return True
            else:
                reason_str = ", ".join(err_reasons)
                if "Bad credentials" in reason_str:
                    _cheat_conn_notify(u"⚠️ GitHub Token không hợp lệ hoặc đã hết hạn!")
                elif "Resource not accessible" in reason_str:
                    _cheat_conn_notify(u"⚠️ Token chưa được cấp quyền ghi (Contents: Write) vào kho!")
                else:
                    _cheat_conn_notify(u"⚠️ Lỗi đẩy GitHub: " + reason_str)
                return False
        except (Exception, BaseException) as e:
            ex_name = e.__class__.__name__
            if 'Restart' in ex_name or 'Reload' in ex_name:
                raise
            _cheat_conn_notify(u"⚠️ Lỗi kết nối GitHub: " + str(e))
            return False

    # 4.5 Bỏ qua lỗi và cho phép game tiếp tục chạy
    def cheat_connect_ignore_error():
        try:
            renpy.store._cheat_conn_last_error = None
            if renpy.has_screen("cheat_recovery_modal"):
                renpy.hide_screen("cheat_recovery_modal")
            renpy.restart_interaction()
        except Exception:
            pass

    # 4.5 Bộ lọc bắt lỗi kịch bản toàn cục thông minh & Tự sửa lỗi tức thì
    def _cheat_conn_global_exception_handler(short, full):
        try:
            err_str = str(short) + "\n" + str(full)

            # Ghi nhật ký lỗi vào file cheat_error.log của game hiện tại
            try:
                gdir = _cheat_conn_get_gamedir()
                log_file = os.path.join(gdir, "cheat_error.log")
                with open(log_file, "a") as f:
                    f.write("\n" + "="*50 + "\n")
                    f.write("THỜI ĐIỂM XẢY RA LỖI: %s\n" % time.ctime())
                    f.write(err_str)
                    f.write("\n" + "="*50 + "\n")
            except Exception:
                pass

            renpy.store._cheat_conn_last_error = str(short)
            renpy.store._cheat_conn_error_time = time.time()
            renpy.store._cheat_conn_error_count = getattr(renpy.store, '_cheat_conn_error_count', 0) + 1

            # Kiểm tra định danh hợp lệ
            def _cheat_is_valid_ident(ident_str):
                if not ident_str:
                    return False
                if not (ident_str[0].isalpha() or ident_str[0] == '_'):
                    return False
                for ch in ident_str[1:]:
                    if not (ch.isalnum() or ch == '_'):
                        return False
                return True

            # ------------------------------------------------------------------
            # BỘ MÁY TỰ ĐỘNG SỬA FILE LẬP TỨC (ZERO-CLICK INSTANT AUTO-HEALING)
            # ------------------------------------------------------------------
            gdir = _cheat_conn_get_gamedir()
            repaired = False
            repair_msg = ""

            # A. Tự sửa file cheat_menu.rpy nếu bị lỗi / hỏng cú pháp / xung đột bytecode
            is_cheat_related = any(k in err_str.lower() for k in ['cheat_menu', '00_cheat', 'cheat_connect', 'cheat_floating_bar', 'cheat_main_modal'])
            is_bytecode_error = any(k in err_str.lower() for k in ['bad marshal data', 'magic number', 'eoferror', 'typeerror: function takes at most'])

            if is_bytecode_error or is_cheat_related:
                for c_name in ("cheat_menu.rpyc", "00_cheat_connect.rpyc", "cheat_connect.rpyc"):
                    c_path = os.path.join(gdir, c_name)
                    if os.path.isfile(c_path):
                        try:
                            os.remove(c_path)
                        except Exception:
                            pass

                # Khôi phục chép đè bản sạch trực tiếp từ GitHub ngay lập tức
                target = os.path.join(gdir, "cheat_menu.rpy")
                if _cheat_conn_download_from_github(_cheat_conn_github_menu_url, target):
                    repair_msg = "Đã tự động tải lại bản sạch cheat_menu.rpy từ GitHub và dọn sạch cache bytecode!"
                    repaired = True
                else:
                    repair_msg = "Đã dọn sạch cache bytecode .rpyc xung đột!"
                    repaired = True

            # B. Tự sửa kịch bản game khi bị THIẾU BIẾN (NameError: name 'xxx' is not defined)
            if ("name '" in str(short) or 'name "' in str(short)) and "is not defined" in str(short):
                try:
                    var_name = None
                    if "name '" in str(short):
                        var_name = str(short).split("name '")[1].split("'")[0]
                    elif 'name "' in str(short):
                        var_name = str(short).split('name "')[1].split('"')[0]

                    if var_name and _cheat_is_valid_ident(var_name):
                        setattr(renpy.store, var_name, 0)
                        autofix_file = os.path.join(gdir, "00_cheat_autofix.rpy")
                        with open(autofix_file, "a") as f:
                            f.write("# Tu dong sua loi thieu bien khao sat boi Cheat Connector\n")
                            f.write("default %s = 0\n" % var_name)
                        repair_msg = "Đã tự động khai báo biến thiếu: '%s' = 0 và ghi vào 00_cheat_autofix.rpy!" % var_name
                        repaired = True
                except Exception:
                    pass

            # C. Tự sửa khi bị THIẾU THUỘC TÍNH (AttributeError: ... has no attribute 'xxx')
            if "has no attribute '" in str(short):
                try:
                    attr_name = str(short).split("has no attribute '")[1].split("'")[0]
                    if attr_name and _cheat_is_valid_ident(attr_name):
                        setattr(renpy.store, attr_name, 0)
                        if 'renpy' in err_str.lower():
                            setattr(renpy, attr_name, lambda *a, **k: None)
                        repair_msg = "Đã tự động bù đắp thuộc tính thiếu: '%s'!" % attr_name
                        repaired = True
                except Exception:
                    pass

            # Nếu tự động sửa lỗi thành công -> Thông báo và tiếp tục game mượt mà
            if repaired:
                # Nếu là tác giả/chủ sở hữu (có token GitHub trong github_token.txt), tự động đồng bộ bản vá lên GitHub!
                if _cheat_conn_get_github_token():
                    try:
                        ok_push, _ = _cheat_conn_push_single_file("cheat_menu.rpy", "Tu dong dong bo ban sua loi tu game [skip ci]")
                        if ok_push:
                            repair_msg += " (Đã tự động đẩy lên GitHub!)"
                    except Exception:
                        pass
                _cheat_conn_notify("⚡ [Tự Động Sửa Lập Tức] " + repair_msg)
                return True

            # Hiển thị màn hình cứu hộ nếu là lỗi phức tạp
            try:
                if hasattr(renpy, 'show_screen'):
                    renpy.show_screen('cheat_recovery_modal', error_msg=str(short))
                    return True
            except Exception:
                pass
        except Exception:
            pass

        return False

    # Đăng ký bộ xử lý ngoại lệ vào Ren'Py config
    try:
        if hasattr(renpy, 'config'):
            renpy.config.exception_handler = _cheat_conn_global_exception_handler
    except Exception:
        pass


# ------------------------------------------------------------------------------
# 5. ĐẢM BẢO HOẠT ĐỘNG NGAY LẦN CHẠY 1 (DUAL INSTANT ACTIVATION ENGINE)
# ------------------------------------------------------------------------------
init 999 python:
    _conn_always = getattr(renpy.config, 'always_shown_screens', None)
    if _conn_always is not None and isinstance(_conn_always, list):
        if 'cheat_connect_global_keys' not in _conn_always:
            _conn_always.append('cheat_connect_global_keys')

    _conn_overlay = getattr(renpy.config, 'overlay_screens', None)
    if _conn_overlay is not None and isinstance(_conn_overlay, list):
        if 'cheat_connect_global_keys' not in _conn_overlay:
            _conn_overlay.append('cheat_connect_global_keys')

    # Cơ chế Cứu Hộ Dự Phòng: Tự reload 1 lần ngầm nếu Ren'Py yêu cầu biên dịch lại
    def _cheat_conn_verify_loaded():
        try:
            has_file = os.path.isfile(_cheat_conn_target_file)
            screen_loaded = False
            try:
                screen_loaded = renpy.has_screen('cheat_floating_bar') or renpy.has_screen('cheat_main_modal')
            except Exception:
                screen_loaded = False

            if has_file and not screen_loaded:
                if hasattr(renpy, 'session') and not renpy.session.get('_cheat_conn_reloaded_once', False):
                    renpy.session['_cheat_conn_reloaded_once'] = True
                    _cheat_conn_log("Auto-activating cheat menu via 1-time instant reload...")
                    cheat_conn_clean_restart()
                    return

            if not renpy.get_screen('cheat_connect_global_keys'):
                renpy.show_screen('cheat_connect_global_keys')
        except (Exception, BaseException) as e:
            ex_name = e.__class__.__name__
            if 'Restart' in ex_name or 'Reload' in ex_name:
                raise

    _cheat_conn_verify_loaded()

    for cb_name in ('start_callbacks', 'after_load_callbacks', 'interact_callbacks'):
        c_list = getattr(renpy.config, cb_name, None)
        if c_list is not None and isinstance(c_list, list) and _cheat_conn_verify_loaded not in c_list:
            c_list.append(_cheat_conn_verify_loaded)


# ------------------------------------------------------------------------------
# 6. GIAO DIỆN PHÍM TẮT TOÀN CỤC & BẢNG CỨU HỘ SỬA LỖI (PREMIUM MODAL UI)
# ------------------------------------------------------------------------------

# 6.1 Màn hình phím tắt toàn cầu (Global Hotkeys)
screen cheat_connect_global_keys():
    zorder 2500
    # Shift + F11: Ép Cập nhật từ GitHub và Tự sửa lỗi
    key 'shift_K_F11' action Function(cheat_connect_force_update)
    key 'alt_shift_K_c' action Function(cheat_connect_force_update)

    # Shift + F10: Xóa sạch cache bytecode .rpyc và khởi động lại
    key 'shift_K_F10' action Function(cheat_connect_clean_cache_and_restart)

    # Ctrl + Shift + F12: Đẩy bản sửa lỗi cheat_menu.rpy lên GitHub qua API
    key 'ctrl_shift_K_F12' action Function(cheat_connect_push_to_github)
    key 'alt_shift_K_F12' action Function(cheat_connect_push_to_github)


# 6.2 Màn hình cứu hộ và sửa lỗi tự động chuyên nghiệp (Glassmorphism Dark UI)
screen cheat_recovery_modal(error_msg=""):
    zorder 3000
    modal True

    frame:
        align (0.5, 0.5)
        xsize 740
        ysize 510
        background "#0f172aee"
        padding (25, 20)

        vbox:
            spacing 12
            xfill True
            yfill True

            # --- TIÊU ĐỀ BẢNG CỨU HỘ ---
            hbox:
                xfill True
                spacing 10
                yalign 0.5
                text "⚠️ BỘ CỨU HỘ & SỬA LỖI REN'PY (GITHUB CLOUD EDITION)" size 16 bold True color "#38bdf8"
                textbutton "✕":
                    xalign 1.0
                    action Function(cheat_connect_ignore_error)
                    text_size 14
                    text_color "#94a3b8"
                    text_hover_color "#f43f5e"

            # --- NỘI DUNG THÔNG BÁO LỖI ---
            frame:
                xfill True
                ysize 140
                background "#1e293bcc"
                padding (12, 10)
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    vbox:
                        spacing 6
                        text "Phát hiện sự cố kịch bản trong quá trình chạy game:" size 12 bold True color "#fbbf24"
                        text (error_msg or getattr(renpy.store, '_cheat_conn_last_error', "Không có chi tiết lỗi.")) size 11 color "#e2e8f0" substitute False

            # --- HƯỚNG DẪN KHẮC PHỤC ---
            text "Chọn phương án cứu hộ bên dưới để tiếp tục mà không làm mất tiến trình chơi:" size 11 italic True color "#94a3b8"

            # --- CÁC NÚT HÀNH ĐỘNG 1-CLICK ---
            vbox:
                spacing 8
                xfill True

                # Nút 1: Cập nhật lại từ GitHub & Sửa lỗi
                button:
                    action Function(cheat_connect_force_update)
                    xfill True
                    ysize 36
                    background "#0284c7"
                    hover_background "#0ea5e9"
                    padding (10, 6)
                    hbox:
                        spacing 8
                        align (0.5, 0.5)
                        text "⚡ [Khuyên Dùng] Tải từ GitHub & Tự sửa lỗi ngay lập tức (Shift + F11)" size 12 bold True color "#ffffff"

                # Nút 2: Xóa sạch cache bytecode .rpyc và Recompile
                button:
                    action Function(cheat_connect_clean_cache_and_restart)
                    xfill True
                    ysize 32
                    background "#334155"
                    hover_background "#475569"
                    padding (10, 6)
                    hbox:
                        spacing 8
                        align (0.5, 0.5)
                        text "🧹 Xóa sạch Cache Bytecode (.rpyc) và Tải lại (Shift + F10)" size 11 bold True color "#cbd5e1"

                # Nút 3: Đẩy bản sửa lỗi lên GitHub qua API (Dành cho Chủ sở hữu / Modder)
                button:
                    action Function(cheat_connect_push_to_github)
                    xfill True
                    ysize 32
                    background "#059669"
                    hover_background "#10b981"
                    padding (10, 6)
                    hbox:
                        spacing 8
                        align (0.5, 0.5)
                        text "🚀 [Chủ Sở Hữu] Đẩy bản sửa lỗi lên GitHub qua API (Ctrl + Shift + F12)" size 11 bold True color "#ffffff"

                # Nút 4: Mở trang GitHub chính thức của dự án
                button:
                    action Function(cheat_connect_open_github)
                    xfill True
                    ysize 30
                    background "#1e293b"
                    hover_background "#334155"
                    padding (8, 4)
                    hbox:
                        spacing 8
                        align (0.5, 0.5)
                        text "🌐 Mở trang GitHub: github.com/Yudy007/Cheat_Menu_Ren-py" size 11 color "#94a3b8"

                # Hàng nút phụ: Bỏ qua lỗi & Rollback
                hbox:
                    xfill True
                    spacing 10
                    button:
                        action Function(cheat_connect_ignore_error)
                        xsize 340
                        ysize 30
                        background "#15803d"
                        hover_background "#16a34a"
                        padding (8, 4)
                        text "🛡️ Bỏ qua lỗi & Tiếp tục chơi" size 11 bold True color "#ffffff" align (0.5, 0.5)

                    button:
                        action Rollback()
                        xsize 340
                        ysize 30
                        background "#475569"
                        hover_background "#64748b"
                        padding (8, 4)
                        text "⏪ Quay lại lượt trước (Rollback)" size 11 bold True color "#ffffff" align (0.5, 0.5)
