# -*- coding: utf-8 -*-
# ==============================================================================
# CHEAT MENU & HIDE-SKIP PRO FOR REN'PY (UNIVERSAL ALL-IN-ONE MOD v3.1)
# ==============================================================================
# Tương thích hoàn hảo: Ren'Py 7 (Python 2.7) & Ren'Py 8 (Python 3)
# ==============================================================================

# ------------------------------------------------------------------------------
# 0. BỘ CỨU HỘ & TỰ ĐỘNG KHẮC PHỤC DỮ LIỆU PERSISTENT (AUTO-REPAIR ENGINE)
# ------------------------------------------------------------------------------
python early:
    import sys
    try:
        import types
    except Exception:
        pass

    # 0.1 Polyfill các decorator/hàm tối ưu hóa của Ren'Py 7.5+ / Ren'Py 8+
    # Khắc phục triệt để lỗi: AttributeError: 'module' object has no attribute 'pure'
    # khi chạy game trên nền Ren'Py 7.4.x (hoặc cũ hơn) mà file 00action_data.rpy có gắn @renpy.pure
    try:
        import renpy

        # Tự động ánh xạ toàn bộ renpy.exports sang module renpy (chuẩn hóa giống Ren'Py 7.5+/8+)
        # Khắc phục triệt để lỗi: AttributeError: 'module' object has no attribute 'Displayable' / 'Render' / 'ParameterizedText'
        # và lỗi AttributeError: _Feature instance has no __call__ method (do Python 2 __future__ with_statement)
        try:
            import renpy.exports as _renpy_exports
            _skip_modules = set(['audio', 'display', 'loader', 'parser', 'ui', 'styledata', 'text', 'gl', 'gl2', 'test', 'sl2', 'compat', 'curry', 'dump'])
            for _k, _v in _renpy_exports.__dict__.items():
                if _k.startswith('__') or _k in _skip_modules:
                    continue
                _curr = getattr(renpy, _k, None)
                if _curr is None:
                    setattr(renpy, _k, _v)
                elif getattr(_curr, '__class__', None) and _curr.__class__.__name__ == '_Feature':
                    setattr(renpy, _k, _v)

            if hasattr(_renpy_exports, 'with_statement'):
                renpy.with_statement = _renpy_exports.with_statement
        except Exception:
            pass

        # Ánh xạ các displayable và renderer cốt lõi
        try:
            import renpy.display.core as _disp_core
            if not hasattr(renpy, 'Displayable'):
                renpy.Displayable = _disp_core.Displayable
            if not hasattr(renpy, 'IgnoreEvent'):
                renpy.IgnoreEvent = _disp_core.IgnoreEvent
        except Exception:
            pass

        try:
            import renpy.display.render as _disp_render
            if not hasattr(renpy, 'Render'):
                renpy.Render = _disp_render.Render
        except Exception:
            pass

        try:
            import renpy.display.behavior as _disp_behavior
            if not hasattr(renpy, 'Keymap'):
                renpy.Keymap = _disp_behavior.Keymap
        except Exception:
            pass

        # Chuyển đổi renpy.curry và renpy.dump từ module thành callable function giữ nguyên thuộc tính module
        # Khắc phục lỗi: TypeError: 'module' object is not callable trong 00layout.rpy:52
        try:
            import renpy.curry as _curry_mod
            if not callable(renpy.curry):
                _curry_fn = _curry_mod.curry
                _curry_fn.curry = _curry_fn
                for _attr in dir(_curry_mod):
                    if not hasattr(_curry_fn, _attr):
                        try:
                            setattr(_curry_fn, _attr, getattr(_curry_mod, _attr))
                        except Exception:
                            pass
                renpy.curry = _curry_fn
        except Exception:
            pass

        try:
            import renpy.dump as _dump_mod
            if not callable(renpy.dump):
                _dump_fn = _dump_mod.dump
                _dump_fn.dump = _dump_fn
                for _attr in dir(_dump_mod):
                    if not hasattr(_dump_fn, _attr):
                        try:
                            setattr(_dump_fn, _attr, getattr(_dump_mod, _attr))
                        except Exception:
                            pass
                renpy.dump = _dump_fn
        except Exception:
            pass

        # Chuyển đổi renpy.rollback từ module thành callable function giữ nguyên thuộc tính module
        # Khắc phục triệt để lỗi: TypeError: 'module' object is not callable khi lăn chuột hoặc gọi renpy.rollback
        try:
            import renpy.rollback as _rollback_mod
            if not callable(renpy.rollback):
                import renpy.exports as _renpy_exports
                _rb_fn = getattr(_renpy_exports, 'rollback', None)
                if _rb_fn is not None:
                    def _safe_rollback_caller(*args, **kwargs):
                        return _rb_fn(*args, **kwargs)
                    for _attr in dir(_rollback_mod):
                        if not hasattr(_safe_rollback_caller, _attr):
                            try:
                                setattr(_safe_rollback_caller, _attr, getattr(_rollback_mod, _attr))
                            except Exception:
                                pass
                    renpy.rollback = _safe_rollback_caller
                    if hasattr(renpy, 'exports'):
                        renpy.exports.rollback = _safe_rollback_caller
        except Exception:
            pass

        # Chuyển đổi renpy.error từ module thành callable function giữ nguyên thuộc tính module
        # Khắc phục triệt để lỗi: TypeError: 'module' object is not callable khi gọi renpy.error(...)
        try:
            import renpy.error as _error_mod
            if not callable(renpy.error):
                import renpy.exports as _renpy_exports
                _err_fn = getattr(_renpy_exports, 'error', None)
                def _safe_error_caller(*args, **kwargs):
                    if _err_fn is not None and callable(_err_fn):
                        try:
                            return _err_fn(*args, **kwargs)
                        except Exception:
                            pass
                    try:
                        if hasattr(renpy, 'log'):
                            renpy.log("ERROR: " + " ".join(str(a) for a in args))
                    except Exception:
                        pass
                    return None
                for _attr in dir(_error_mod):
                    if not hasattr(_safe_error_caller, _attr):
                        try:
                            setattr(_safe_error_caller, _attr, getattr(_error_mod, _attr))
                        except Exception:
                            pass
                renpy.error = _safe_error_caller
                if hasattr(renpy, 'exports'):
                    renpy.exports.error = _safe_error_caller
        except Exception:
            pass

        # Chuyển đổi và bọc renpy.notify an toàn tuyệt đối
        # Khắc phục lỗi: Exception("Hide may not run while in init phase.") trên Ren'Py 7
        # và IndexError: list index out of range (Detached stack[-1]) trên Ren'Py 8
        try:
            import renpy.exports as _renpy_exports
            _orig_notify = getattr(_renpy_exports, 'notify', None)
            if _orig_notify is not None and not getattr(_orig_notify, '_cheat_safe_wrapped', False):
                def _safe_renpy_notify(message, *args, **kwargs):
                    try:
                        if hasattr(renpy, 'game') and hasattr(renpy.game, 'context'):
                            ctx = renpy.game.context()
                            if getattr(ctx, 'init_phase', False):
                                return None
                    except Exception:
                        pass
                    try:
                        return _orig_notify(message, *args, **kwargs)
                    except Exception:
                        return None
                _safe_renpy_notify._cheat_safe_wrapped = True
                renpy.notify = _safe_renpy_notify
                if hasattr(renpy, 'exports'):
                    renpy.exports.notify = _safe_renpy_notify
        except Exception:
            pass

        # Khắc phục triệt để lỗi: Exception("Invalid key specifier wheelup") / wheeldown
        # trên Ren'Py 8.1+ / 8.5+ khi biên dịch sự kiện phím chuột
        try:
            import renpy.display.behavior as _disp_bh
            if hasattr(_disp_bh, 'compile_event'):
                _orig_compile_event = getattr(_disp_bh, 'compile_event', None)
                if _orig_compile_event is not None and not getattr(_orig_compile_event, '_cheat_safe_compiled', False):
                    def _safe_compile_event(key, keydown):
                        if key == 'wheelup':
                            return _orig_compile_event('mousedown_4', keydown)
                        elif key == 'wheeldown':
                            return _orig_compile_event('mousedown_5', keydown)
                        try:
                            return _orig_compile_event(key, keydown)
                        except Exception:
                            return "(False)"
                    _safe_compile_event._cheat_safe_compiled = True
                    _disp_bh.compile_event = _safe_compile_event
        except Exception:
            pass

        try:
            if hasattr(renpy, 'config') and hasattr(renpy.config, 'key_aliases') and isinstance(renpy.config.key_aliases, dict):
                renpy.config.key_aliases['wheelup'] = 'mousedown_4'
                renpy.config.key_aliases['wheeldown'] = 'mousedown_5'
        except Exception:
            pass

        # Khắc phục lỗi KeyError trong check_image khi game có image khai báo thiếu hoặc live2d (như tameit)
        try:
            import renpy.display.image as _disp_image
            if hasattr(_disp_image, 'images') and isinstance(_disp_image.images, dict):
                class _SafeImageDict(dict):
                    def __missing__(self, key):
                        return None
                if not isinstance(_disp_image.images, _SafeImageDict):
                    _safe_img_dict = _SafeImageDict(_disp_image.images)
                    _disp_image.images = _safe_img_dict
        except Exception:
            pass

        # Bảo vệ toàn diện hành vi run(action): Khắc phục triệt để TypeError: 'module' object is not callable
        try:
            import renpy.display.behavior as _disp_bh
            if not getattr(_disp_bh, '_cheat_safe_run_installed', False):
                _orig_behavior_run = _disp_bh.run
                def _cheat_safe_behavior_run(action, *args, **kwargs):
                    if action is None:
                        return None
                    if isinstance(action, (list, tuple)):
                        rv = None
                        for i in action:
                            new_rv = _cheat_safe_behavior_run(i, *args, **kwargs)
                            if new_rv is not None:
                                rv = new_rv
                        return rv
                    # Nếu action là module (đặc biệt là module renpy.rollback)
                    if 'types' in globals() and hasattr(types, 'ModuleType') and isinstance(action, types.ModuleType):
                        if getattr(action, '__name__', '') == 'renpy.rollback':
                            try:
                                return renpy.exports.rollback(*args, **kwargs)
                            except Exception:
                                return None
                        return None
                    if not callable(action):
                        return None
                    return _orig_behavior_run(action, *args, **kwargs)
                _disp_bh.run = _cheat_safe_behavior_run
                _disp_bh._cheat_safe_run_installed = True
        except Exception:
            pass

        # Khắc phục triệt để lỗi: Exception("Could not find font ...")
        # (Đặc biệt là 'AI_trans_pry/font/font.ttf' hoặc các font mod dịch thuật bị thiếu)
        try:
            import renpy.text.font as _font_mod
            if hasattr(_font_mod, 'load_face'):
                _orig_load_face = _font_mod.load_face
                if not getattr(_orig_load_face, '_cheat_safe_font_hooked', False):
                    def _safe_load_face(fn, *args, **kwargs):
                        try:
                            return _orig_load_face(fn, *args, **kwargs)
                        except Exception as _orig_err:
                            _fallback_candidates = ("font.ttf", "DejaVuSans.ttf", "Cinzel-Regular.ttf")
                            for _fb in _fallback_candidates:
                                if _fb != fn:
                                    try:
                                        return _orig_load_face(_fb, *args, **kwargs)
                                    except Exception:
                                        pass
                            raise _orig_err
                    _safe_load_face._cheat_safe_font_hooked = True
                    _font_mod.load_face = _safe_load_face
        except Exception:
            pass

        # Dự phòng IAP và Watchers
        if not hasattr(renpy, 'iap'):
            try:
                import renpy.iap as _iap_mod
                renpy.iap = _iap_mod
            except Exception:
                class _DummyIAP(object):
                    @staticmethod
                    def is_purchased(*a, **k): return False
                    @staticmethod
                    def has_purchased(*a, **k): return False
                    @staticmethod
                    def purchase(*a, **k): return False
                    @staticmethod
                    def restore(*a, **k): return False
                renpy.iap = _DummyIAP()

        for watch_fn in ('watch', 'unwatch', 'unwatchall'):
            if not hasattr(renpy, watch_fn):
                setattr(renpy, watch_fn, lambda *a, **k: None)

        def _cheat_pure(*args, **kwargs):
            if not args:
                return lambda fn: fn
            fn = args[0]
            try:
                if hasattr(renpy, 'pure_functions') and isinstance(renpy.pure_functions, set):
                    renpy.pure_functions.add(fn)
                    if hasattr(fn, '__name__'):
                        renpy.pure_functions.add(fn.__name__)
            except Exception:
                pass
            return fn

        def _cheat_noop_decorator(*args, **kwargs):
            if not args:
                return lambda fn: fn
            return args[0]

        if not hasattr(renpy, 'pure'):
            renpy.pure = _cheat_pure
        if not hasattr(renpy, 'const'):
            renpy.const = _cheat_noop_decorator
        if not hasattr(renpy, 'not_const'):
            renpy.not_const = _cheat_noop_decorator
        if not hasattr(renpy, 'pure_functions'):
            renpy.pure_functions = set()

        if hasattr(renpy, 'python'):
            if not hasattr(renpy.python, 'pure'):
                renpy.python.pure = renpy.pure
            if not hasattr(renpy.python, 'const'):
                renpy.python.const = renpy.const
            if not hasattr(renpy.python, 'not_const'):
                renpy.python.not_const = renpy.not_const

        try:
            import renpy.store as store
            for attr in ('pure', 'const', 'not_const'):
                if not hasattr(store, attr):
                    setattr(store, attr, _cheat_noop_decorator)
            if not hasattr(store, 'FieldEquality'):
                class FieldEquality(object):
                    identity_fields = ()
                    equality_fields = ()
                store.FieldEquality = FieldEquality
        except Exception:
            pass

        # 0.1.2 Đảm bảo renpy.music, renpy.sound, renpy.audio, renpy.voice luôn tồn tại
        # Khắc phục triệt để lỗi: AttributeError: 'module' object has no attribute 'music'
        # khi chạy game trên nền Ren'Py 7.4.x mà file 00mixers.rpy (hoặc common script mới) gọi renpy.music ở init -1600
        if not hasattr(renpy, 'music') or renpy.music is None:
            try:
                import renpy.audio.music as _audio_music
                renpy.music = _audio_music
            except Exception:
                pass

        if not hasattr(renpy, 'sound') or renpy.sound is None:
            try:
                import renpy.audio.sound as _audio_sound
                renpy.sound = _audio_sound
            except Exception:
                pass

        if not hasattr(renpy, 'audio') or renpy.audio is None:
            try:
                import renpy.audio.audio as _audio_audio
                renpy.audio = _audio_audio
            except Exception:
                pass

        if not hasattr(renpy, 'voice') or renpy.voice is None:
            try:
                import renpy.audio.voice as _audio_voice
                renpy.voice = _audio_voice
            except Exception:
                pass

        # Cung cấp Dummy Music fallback nếu renpy.music vẫn thiếu hoặc không có register_channel
        if not hasattr(renpy, 'music') or not hasattr(renpy.music, 'register_channel'):
            class _CheatDummyMusic(object):
                @staticmethod
                def register_channel(*args, **kwargs):
                    pass
                @staticmethod
                def play(*args, **kwargs):
                    pass
                @staticmethod
                def stop(*args, **kwargs):
                    pass
                @staticmethod
                def queue(*args, **kwargs):
                    pass
                @staticmethod
                def set_volume(*args, **kwargs):
                    pass
                @staticmethod
                def get_playing(*args, **kwargs):
                    return None
                @staticmethod
                def get_pos(*args, **kwargs):
                    return None
            renpy.music = _CheatDummyMusic()

        if not hasattr(renpy, 'sound') or renpy.sound is None:
            renpy.sound = renpy.music

        try:
            import renpy.store as store
            if not hasattr(store, 'music') and hasattr(renpy, 'music'):
                store.music = renpy.music
            if not hasattr(store, 'sound') and hasattr(renpy, 'sound'):
                store.sound = renpy.sound
        except Exception:
            pass

        # 0.1.3 Polyfill cho các hàm đăng ký hệ thống mới (renpy.register_persistent, register_shader, fetch,...)
        # Khắc phục triệt để lỗi: AttributeError: 'module' object has no attribute 'register_persistent'
        # khi chạy 00achievement.rpy hoặc các file common từ Ren'Py 7.5+/8+
        if not hasattr(renpy, 'register_persistent'):
            def _cheat_register_persistent(field_name, merge_function=None):
                try:
                    if not hasattr(renpy, '_persistent_callbacks'):
                        renpy._persistent_callbacks = {}
                    if merge_function is not None:
                        renpy._persistent_callbacks[field_name] = merge_function
                except Exception:
                    pass
            renpy.register_persistent = _cheat_register_persistent

        if not hasattr(renpy, 'register_shader'):
            def _cheat_register_shader(*args, **kwargs):
                pass
            renpy.register_shader = _cheat_register_shader

        if not hasattr(renpy, 'fetch'):
            def _cheat_fetch(*args, **kwargs):
                return None
            renpy.fetch = _cheat_fetch

        if not hasattr(renpy, 'register_sl_displayable'):
            class _CheatSLDisplayable(object):
                def add_positional(self, *a, **k): return self
                def add_property(self, *a, **k): return self
                def add_style_property(self, *a, **k): return self
                def add_prefix_style_property(self, *a, **k): return self
                def add_property_group(self, *a, **k): return self
                def copy_properties(self, *a, **k): return self
            def _cheat_register_sl_displayable(*args, **kwargs):
                return _CheatSLDisplayable()
            renpy.register_sl_displayable = _cheat_register_sl_displayable

        if not hasattr(renpy, 'write_log'):
            def _cheat_write_log(msg, *args, **kwargs):
                try:
                    if hasattr(renpy, 'log'):
                        if args:
                            renpy.log(msg % args)
                        else:
                            renpy.log(msg)
                except Exception:
                    pass
            renpy.write_log = _cheat_write_log

        if not hasattr(renpy, 'log'):
            renpy.log = lambda *args, **kwargs: None

        if not hasattr(renpy, 'invoke_in_thread'):
            def _cheat_invoke_in_thread(fn, *args, **kwargs):
                import threading
                t = threading.Thread(target=fn, args=args, kwargs=kwargs)
                t.daemon = True
                t.start()
                return t
            renpy.invoke_in_thread = _cheat_invoke_in_thread

        if not hasattr(renpy, 'invoke_in_main_thread'):
            def _cheat_invoke_in_main_thread(fn, *args, **kwargs):
                return fn(*args, **kwargs)
            renpy.invoke_in_main_thread = _cheat_invoke_in_main_thread

        # 0.1.4 Polyfill cho ParameterizedText và các Displayable trên renpy
        # Khắc phục lỗi: AttributeError: 'module' object has no attribute 'ParameterizedText' trong 00defaults.rpy
        if not hasattr(renpy, 'ParameterizedText'):
            try:
                import renpy.text.extras as _text_extras
                renpy.ParameterizedText = _text_extras.ParameterizedText
            except Exception:
                try:
                    import renpy.display.text as _disp_text
                    renpy.ParameterizedText = getattr(_disp_text, 'ParameterizedText', None)
                except Exception:
                    pass

        if not hasattr(renpy, 'ParameterizedText') or renpy.ParameterizedText is None:
            try:
                import renpy.store as store
                if hasattr(store, 'ParameterizedText'):
                    renpy.ParameterizedText = store.ParameterizedText
            except Exception:
                pass

        if not hasattr(renpy, 'ParameterizedText') or renpy.ParameterizedText is None:
            try:
                class _CheatParameterizedText(renpy.Displayable):
                    def __init__(self, style='default', **properties):
                        super(_CheatParameterizedText, self).__init__(style=style, **properties)
                    def __call__(self, text, **properties):
                        try:
                            return renpy.display.text.Text(text, **properties)
                        except Exception:
                            return None
                renpy.ParameterizedText = _CheatParameterizedText
            except Exception:
                class _CheatParameterizedText(object):
                    def __init__(self, *a, **k): pass
                    def __call__(self, *a, **k): return None
                renpy.ParameterizedText = _CheatParameterizedText

        # Đảm bảo các displayable phổ biến luôn có mặt trên renpy nếu common script mới gọi renpy.<Displayable>
        for disp_name in ('ParameterizedText', 'Text', 'Solid', 'Frame', 'Image', 'Composite', 'LiveComposite', 'DynamicDisplayable', 'ConditionSwitch', 'Transform', 'Null', 'Fixed'):
            if not hasattr(renpy, disp_name):
                try:
                    import renpy.store as store
                    if hasattr(store, disp_name):
                        setattr(renpy, disp_name, getattr(store, disp_name))
                except Exception:
                    pass

        # 0.1.5 Polyfill cho renpy.show_display_say và các hàm giao diện/cấu hình mới
        # Khắc phục lỗi: AttributeError: 'module' object has no attribute 'show_display_say' trong 00nvl_mode.rpy
        if not hasattr(renpy, 'show_display_say'):
            try:
                import renpy.character as _character_mod
                renpy.show_display_say = _character_mod.show_display_say
            except Exception:
                try:
                    import renpy.exports as _exports_mod
                    renpy.show_display_say = getattr(_exports_mod, 'show_display_say', None)
                except Exception:
                    pass

        if not hasattr(renpy, 'show_display_say') or renpy.show_display_say is None:
            def _cheat_show_display_say(who, what, **kwargs):
                try:
                    import renpy.character as _character_mod
                    return _character_mod.show_display_say(who, what, **kwargs)
                except Exception:
                    try:
                        return renpy.display_say(who, what, **kwargs)
                    except Exception:
                        return None
            renpy.show_display_say = _cheat_show_display_say

        if not hasattr(renpy, 'predict_show_display_say'):
            try:
                import renpy.character as _character_mod
                renpy.predict_show_display_say = _character_mod.predict_show_display_say
            except Exception:
                renpy.predict_show_display_say = lambda *a, **k: None

        # Style preferences API
        if not hasattr(renpy, 'register_style_preference'):
            try:
                import renpy.style as _style_mod
                renpy.register_style_preference = getattr(_style_mod, 'register_style_preference', lambda *a, **k: None)
            except Exception:
                renpy.register_style_preference = lambda *a, **k: None

        if not hasattr(renpy, 'get_style_preference'):
            try:
                import renpy.style as _style_mod
                renpy.get_style_preference = getattr(_style_mod, 'get_style_preference', lambda *a, **k: "")
            except Exception:
                renpy.get_style_preference = lambda *a, **k: ""

        if not hasattr(renpy, 'set_style_preference'):
            try:
                import renpy.style as _style_mod
                renpy.set_style_preference = getattr(_style_mod, 'set_style_preference', lambda *a, **k: None)
            except Exception:
                renpy.set_style_preference = lambda *a, **k: None

        # Helper & utility functions
        if not hasattr(renpy, 'split_properties'):
            try:
                import renpy.easy as _easy_mod
                renpy.split_properties = _easy_mod.split_properties
            except Exception:
                renpy.split_properties = lambda *a, **k: ({}, {})

        if not hasattr(renpy, 'slot_json'):
            try:
                import renpy.loadsave as _ls_mod
                renpy.slot_json = getattr(_ls_mod, 'slot_json', lambda *a, **k: None)
            except Exception:
                renpy.slot_json = lambda *a, **k: None

        if not hasattr(renpy, 'get_editable_input_value'):
            renpy.get_editable_input_value = lambda *a, **k: None
        if not hasattr(renpy, 'set_editable_input_value'):
            renpy.set_editable_input_value = lambda *a, **k: None

        if not hasattr(renpy, 'check_image_attributes'):
            try:
                import renpy.display.image as _img_mod
                renpy.check_image_attributes = getattr(_img_mod, 'check_image_attributes', lambda *a, **k: None)
            except Exception:
                renpy.check_image_attributes = lambda *a, **k: None

        if not hasattr(renpy, 'get_ordered_image_attributes'):
            try:
                import renpy.display.image as _img_mod
                renpy.get_ordered_image_attributes = getattr(_img_mod, 'get_ordered_image_attributes', lambda *a, **k: None)
            except Exception:
                renpy.get_ordered_image_attributes = lambda *a, **k: None

        for count_fn in ('count_dialogue_blocks', 'count_seen_dialogue_blocks', 'count_newly_seen_dialogue_blocks'):
            if not hasattr(renpy, count_fn):
                setattr(renpy, count_fn, lambda *a, **k: 0)

        if not hasattr(renpy, 'curried_call_in_new_context'):
            try:
                import renpy.curry as _curry_mod
                renpy.curried_call_in_new_context = _curry_mod.curry(renpy.call_in_new_context)
            except Exception:
                renpy.curried_call_in_new_context = lambda *a, **k: None

        if not hasattr(renpy, 'get_parse_errors'):
            try:
                import renpy.parser as _parser_mod
                renpy.get_parse_errors = getattr(_parser_mod, 'get_parse_errors', lambda *a, **k: [])
            except Exception:
                renpy.get_parse_errors = lambda *a, **k: []

        if not hasattr(renpy, 'execute_default_statement'):
            try:
                import renpy.exports as _exp_mod
                renpy.execute_default_statement = getattr(_exp_mod, 'execute_default_statement', lambda *a, **k: None)
            except Exception:
                renpy.execute_default_statement = lambda *a, **k: None

        try:
            import renpy.store as store
            if not hasattr(store, 'register_persistent'):
                store.register_persistent = renpy.register_persistent
            if not hasattr(store, 'write_log'):
                store.write_log = renpy.write_log
            if not hasattr(store, 'ParameterizedText') and hasattr(renpy, 'ParameterizedText'):
                store.ParameterizedText = renpy.ParameterizedText
        except Exception:
            pass
    except Exception:
        pass

    # 0.2 Khắc phục lỗi persistent._seen_* bị biến thành bool gây crash khi save/load
    try:
        _p_mod = sys.modules.get('renpy.persistent')
        if _p_mod and hasattr(_p_mod, 'Persistent'):
            _orig_persistent_update = getattr(_p_mod.Persistent, '_update', None)
            def _cheat_safe_persistent_update(self):
                # Tự động cứu hộ nếu các biến hệ thống Ren'Py bị biến thành bool
                for attr in ('_seen_audio', '_seen_images', '_seen_ever', '_seen_translates'):
                    val = getattr(self, attr, None)
                    if val is not None and not isinstance(val, (set, dict, list, tuple)):
                        setattr(self, attr, {})
                if _orig_persistent_update:
                    return _orig_persistent_update(self)
            _p_mod.Persistent._update = _cheat_safe_persistent_update
    except Exception:
        pass

    # 0.3 Khắc phục triệt để lỗi IndexError khi cheat stat vượt quá độ dài mảng dữ liệu (như j.pay[j.skill], Job_level[j.skill])
    try:
        import renpy.python
        if hasattr(renpy.python, 'RevertableList') and not getattr(renpy.python.RevertableList, '_cheat_safe_getitem_installed', False):
            _orig_rev_list_getitem = renpy.python.RevertableList.__getitem__
            def _safe_rev_list_getitem(self, index):
                try:
                    return _orig_rev_list_getitem(self, index)
                except IndexError:
                    if len(self) > 0:
                        try:
                            _idx_types = (int, long)
                        except NameError:
                            _idx_types = (int,)
                        if isinstance(index, _idx_types):
                            if index >= len(self):
                                return list.__getitem__(self, -1)
                            elif index < -len(self):
                                return list.__getitem__(self, 0)
                    raise
            renpy.python.RevertableList.__getitem__ = _safe_rev_list_getitem
            renpy.python.RevertableList._cheat_safe_getitem_installed = True
    except Exception:
        pass

init -999 python:
    import sys
    import os
    import re
    import time
    import json
    import threading

    try:
        import renpy.exports as _renpy_exports
        if hasattr(_renpy_exports, 'with_statement'):
            renpy.with_statement = _renpy_exports.with_statement
    except Exception:
        pass

    try:
        import renpy.error as _error_mod
        if not callable(renpy.error):
            import renpy.exports as _renpy_exports
            _err_fn = getattr(_renpy_exports, 'error', None)
            def _safe_error_caller(*args, **kwargs):
                if _err_fn is not None and callable(_err_fn):
                    try:
                        return _err_fn(*args, **kwargs)
                    except Exception:
                        pass
                return None
            for _attr in dir(_error_mod):
                if not hasattr(_safe_error_caller, _attr):
                    try:
                        setattr(_safe_error_caller, _attr, getattr(_error_mod, _attr))
                    except Exception:
                        pass
            renpy.error = _safe_error_caller
            if hasattr(renpy, 'exports'):
                renpy.exports.error = _safe_error_caller
    except Exception:
        pass

    # Khắc phục lỗi KeyError trong check_image khi game có image khai báo thiếu hoặc live2d (như tameit)
    try:
        import renpy.display.image as _disp_image
        if hasattr(_disp_image, 'images') and isinstance(_disp_image.images, dict):
            class _SafeImageDict(dict):
                def __missing__(self, key):
                    return None
                def __getitem__(self, key):
                    try:
                        return dict.__getitem__(self, key)
                    except KeyError:
                        return None
            if not isinstance(_disp_image.images, _SafeImageDict):
                _disp_image.images = _SafeImageDict(_disp_image.images)
    except Exception:
        pass

    try:
        import renpy.lint as _lint_mod
        if hasattr(_lint_mod, 'check_image'):
            _orig_check_image = _lint_mod.check_image
            def _safe_check_image(node):
                try:
                    return _orig_check_image(node)
                except KeyError:
                    pass
            _lint_mod.check_image = _safe_check_image
    except Exception:
        pass

    try:
        import types
        import renpy.display.behavior as _disp_bh
        if not getattr(_disp_bh, '_cheat_safe_run_installed', False):
            _orig_bh_run = _disp_bh.run
            def _cheat_safe_behavior_run(action, *args, **kwargs):
                if action is None:
                    return None
                if isinstance(action, (list, tuple)):
                    rv = None
                    for i in action:
                        new_rv = _cheat_safe_behavior_run(i, *args, **kwargs)
                        if new_rv is not None:
                            rv = new_rv
                    return rv
                if hasattr(types, 'ModuleType') and isinstance(action, types.ModuleType):
                    if getattr(action, '__name__', '') == 'renpy.rollback':
                        try:
                            return renpy.exports.rollback(*args, **kwargs)
                        except Exception:
                            return None
                    return None
                if not callable(action):
                    return None
                return _orig_bh_run(action, *args, **kwargs)
            _disp_bh.run = _cheat_safe_behavior_run
            _disp_bh._cheat_safe_run_installed = True
    except Exception:
        pass

    # --------------------------------------------------------------------------
    # 1. HỖ TRỢ ĐA PHIÊN BẢN PYTHON 2 & 3 / REN'PY 6, 7 & 8
    # --------------------------------------------------------------------------
    PY3 = sys.version_info[0] >= 3

    try:
        _INT_TYPES = (int, long)
        _NUM_TYPES = (int, long, float)
    except NameError:
        _INT_TYPES = (int,)
        _NUM_TYPES = (int, float)

    try:
        _STR_TYPES = (str, unicode)
        _UNICODE_TYPE = unicode
    except NameError:
        _STR_TYPES = (str,)
        _UNICODE_TYPE = str

    def _safe_str(val):
        """Chuyển đổi chuỗi an toàn tuyệt đối cho cả Python 2 và 3."""
        if val is None:
            return ""
        try:
            if PY3:
                return str(val)
            else:
                if isinstance(val, _UNICODE_TYPE):
                    return val.encode('utf-8', 'ignore')
                return str(val)
        except Exception:
            return "<value>"

    def _safe_unicode(val):
        if val is None:
            return u""
        try:
            if PY3:
                return str(val)
            else:
                if isinstance(val, str):
                    return val.decode('utf-8', 'ignore')
                return _UNICODE_TYPE(val)
        except Exception:
            return u"<value>"

    def _safe_get_config(name, default=None):
        """Đọc biến config an toàn tuyệt đối, không bao giờ văng lỗi dù config.__getattr__ ném Exception."""
        try:
            return getattr(config, name)
        except Exception:
            return default

    def _safe_set_config(name, val):
        """Gán biến config an toàn, không bao giờ văng lỗi trên bất kỳ bản Ren'Py nào."""
        try:
            setattr(config, name, val)
        except Exception:
            pass

    def _safe_set_pref(name, val):
        """Gán biến preferences an toàn cho cả _preferences và preferences."""
        for p_name in ('_preferences', 'preferences'):
            try:
                p_obj = getattr(renpy.store, p_name, None)
                if p_obj is not None:
                    setattr(p_obj, name, val)
            except Exception:
                pass

    if PY3:
        import urllib.request as urllib_req
        import urllib.parse as urllib_parse
    else:
        import urllib2 as urllib_req
        import urllib as urllib_parse

    # --------------------------------------------------------------------------
    # 1.5. CỐ ĐỊNH PHÔNG CHỮ & STYLE ĐỘC LẬP (STYLE & FONT ISOLATION ENGINE)
    # --------------------------------------------------------------------------
    def cheat_find_unicode_font():
        """
        Tự động thiết lập và sử dụng trực tiếp font.ttf độc lập tuyệt đối cho Cheat Menu.
        Đảm bảo hiển thị hoàn hảo mọi ngôn ngữ và không bao giờ bị ảnh hưởng bởi font của game.
        """
        g_dir = _safe_get_config('gamedir', '.') or '.'
        target_font_name = "font.ttf"
        target_font_path = os.path.join(g_dir, target_font_name)

        # 1. Tự động phát hiện và sao chép font.ttf vào gamedir nếu có ở thư mục script hoặc thư mục gốc
        if not (os.path.isfile(target_font_path) and os.path.getsize(target_font_path) > 1000):
            candidate_dirs = []
            try:
                if '__file__' in globals() and __file__:
                    candidate_dirs.append(os.path.dirname(os.path.abspath(__file__)))
            except Exception:
                pass
            try:
                candidate_dirs.append(os.path.abspath('.'))
                candidate_dirs.append(os.path.join(os.path.abspath('.'), 'game'))
            except Exception:
                pass

            for c_dir in candidate_dirs:
                if not c_dir:
                    continue
                cand_path = os.path.join(c_dir, target_font_name)
                if os.path.isfile(cand_path) and os.path.getsize(cand_path) > 1000:
                    try:
                        import shutil
                        shutil.copyfile(cand_path, target_font_path)
                        break
                    except Exception:
                        pass

        # Tự động đảm bảo thư mục và file font cho module dịch AI_trans_pry nếu cần
        try:
            ai_font_dir = os.path.join(g_dir, "AI_trans_pry", "font")
            ai_font_path = os.path.join(ai_font_dir, "font.ttf")
            if not os.path.isfile(ai_font_path):
                if not os.path.isdir(ai_font_dir):
                    os.makedirs(ai_font_dir)
                if os.path.isfile(target_font_path):
                    import shutil
                    shutil.copyfile(target_font_path, ai_font_path)
        except Exception:
            pass

        # 2. Nếu file font.ttf tồn tại trong gamedir hoặc có thể nạp qua renpy.loadable, dùng ngay!
        if (os.path.isfile(target_font_path) and os.path.getsize(target_font_path) > 1000) or renpy.loadable(target_font_name):
            return target_font_name

        # Thử tìm trong các thư mục con thường gặp như fonts/font.ttf, cheat_menu/font.ttf
        for sub_f in ("fonts/font.ttf", "cheat_menu/font.ttf"):
            try:
                if renpy.loadable(sub_f):
                    return sub_f
            except Exception:
                pass

        # 3. DỰ PHÒNG KHẨN CẤP: Nếu chưa có font.ttf, tự động sao chép font hệ thống thành font.ttf
        if not os.path.exists(target_font_path):
            copied = False
            if sys.platform == 'win32':
                import shutil
                for win_f in ("C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/tahoma.ttf"):
                    if os.path.exists(win_f):
                        try:
                            shutil.copyfile(win_f, target_font_path)
                            copied = True
                            break
                        except Exception:
                            pass

            if not copied:
                for existing_f in ("Cinzel-Regular.ttf", "Cinzel.ttf", "fonts/Cinzel-Regular.ttf"):
                    p = os.path.join(g_dir, existing_f)
                    if os.path.exists(p):
                        try:
                            import shutil
                            shutil.copyfile(p, target_font_path)
                            copied = True
                            break
                        except Exception:
                            pass

        if os.path.exists(target_font_path) or renpy.loadable(target_font_name):
            return target_font_name

        # 4. Fallback sang các font chuẩn Ren'Py có sẵn
        for f in ("DejaVuSans.ttf", "Cinzel-Regular.ttf", "Cinzel.ttf"):
            try:
                if renpy.loadable(f):
                    return f
            except Exception:
                pass

        return "DejaVuSans.ttf"

    cheat_font = cheat_find_unicode_font()

    def cheat_truncate_single_line(val, max_len=16):
        """Chuyển chuỗi thành 1 dòng duy nhất, nếu dài quá thì cắt và thêm dấu ... an toàn Unicode."""
        if not val:
            return u""
        s = _safe_unicode(val).replace(u'\r\n', u' ').replace(u'\n', u' ').replace(u'\r', u' ').strip()
        if len(s) > max_len:
            return s[:max_len - 2] + u"..."
        return s

    def cheat_setup_isolated_styles():
        """
        Thiết lập toàn bộ style của Cheat Menu kế thừa trực tiếp từ style.empty.
        Đảm bảo 100% KHÔNG BAO GIỜ bị ảnh hưởng bởi style.button, style.frame,
        hay font/padding/margin của bất kỳ game nào.
        """
        global cheat_font
        cheat_font = cheat_find_unicode_font()

        styles_to_init = (
            'cheat_default', 'cheat_text', 'cheat_button', 'cheat_button_text',
            'cheat_input', 'cheat_frame', 'cheat_window', 'cheat_vbox', 'cheat_hbox',
            'cheat_grid', 'cheat_label', 'cheat_label_text', 'cheat_viewport'
        )
        for s_name in styles_to_init:
            try:
                setattr(style, s_name, Style(style.empty))
            except Exception:
                pass

        # cheat_vscrollbar kế thừa từ vscrollbar gốc để giữ đầy đủ hành vi thanh cuộn
        if hasattr(style, 'vscrollbar'):
            try:
                style.cheat_vscrollbar = Style(style.vscrollbar)
            except Exception:
                style.cheat_vscrollbar = Style(style.empty)
        else:
            style.cheat_vscrollbar = Style(style.empty)

        # 1. cheat_default
        try:
            if cheat_font:
                style.cheat_default.font = cheat_font
            style.cheat_default.size = 12
            style.cheat_default.color = "#ffffff"
            style.cheat_default.outlines = []
            style.cheat_default.line_spacing = 1
        except Exception:
            pass

        # 2. cheat_text
        try:
            if cheat_font:
                style.cheat_text.font = cheat_font
            style.cheat_text.size = 12
            style.cheat_text.color = "#cbd5e1"
            style.cheat_text.outlines = []
            style.cheat_text.line_spacing = 1
        except Exception:
            pass

        # 3. cheat_button: Xóa sạch padding, margin, kích thước tối thiểu và hình nền từ game
        try:
            style.cheat_button.background = None
            style.cheat_button.hover_background = None
            style.cheat_button.selected_background = None
            style.cheat_button.padding = (0, 0, 0, 0)
            style.cheat_button.margin = (0, 0, 0, 0)
            style.cheat_button.xminimum = 0
            style.cheat_button.yminimum = 0
            style.cheat_button.focus_mask = None
        except Exception:
            pass

        # 4. cheat_button_text: Định hình chữ nút bấm chuẩn mực
        try:
            if cheat_font:
                style.cheat_button_text.font = cheat_font
            style.cheat_button_text.size = 12
            style.cheat_button_text.color = "#ffffff"
            style.cheat_button_text.hover_color = "#38bdf8"
            style.cheat_button_text.selected_color = "#38bdf8"
            style.cheat_button_text.outlines = []
            style.cheat_button_text.line_spacing = 1
        except Exception:
            pass

        # 5. cheat_frame: Chống vỡ khung và chống kế thừa border từ game
        try:
            style.cheat_frame.background = None
            style.cheat_frame.padding = (0, 0, 0, 0)
            style.cheat_frame.margin = (0, 0, 0, 0)
            style.cheat_frame.xminimum = 0
            style.cheat_frame.yminimum = 0
        except Exception:
            pass

        # 6. cheat_window
        try:
            style.cheat_window.background = None
            style.cheat_window.padding = (0, 0, 0, 0)
            style.cheat_window.margin = (0, 0, 0, 0)
        except Exception:
            pass

        # 7. cheat_vbox & cheat_hbox
        try:
            style.cheat_vbox.spacing = 0
            style.cheat_hbox.spacing = 0
        except Exception:
            pass

        # 8. cheat_input
        try:
            if cheat_font:
                style.cheat_input.font = cheat_font
            style.cheat_input.size = 12
            style.cheat_input.color = "#ffffff"
            style.cheat_input.outlines = []
        except Exception:
            pass

        # 9. cheat_label & cheat_label_text
        try:
            style.cheat_label.padding = (0, 0, 0, 0)
            if cheat_font:
                style.cheat_label_text.font = cheat_font
            style.cheat_label_text.size = 12
            style.cheat_label_text.color = "#ffffff"
            style.cheat_label_text.outlines = []
        except Exception:
            pass

        # 10. cheat_viewport & scrollbar
        try:
            style.cheat_viewport.xfill = False
            style.cheat_viewport.yfill = False
        except Exception:
            pass

        try:
            style.cheat_vscrollbar.unscrollable = "hide"
            style.cheat_vscrollbar.xsize = 6
        except Exception:
            pass

    cheat_setup_isolated_styles()

    # --------------------------------------------------------------------------
    # 2. KHỞI TẠO CẤU HÌNH VÀ ÉP SKIP CẢ THOẠI CHƯA ĐỌC (FORCE SKIP)
    # --------------------------------------------------------------------------
    persistent.cm_bar_visible = True
    persistent.cm_bar_collapsed = True
    if persistent.cm_bar_y is None or persistent.cm_bar_y < 10 or persistent.cm_bar_y > 800:
        persistent.cm_bar_y = 140
    # Tắt dịch tự động mặc định khi mở game
    persistent.cm_auto_translate = False
    if persistent.cm_translate_bilingual is None:
        persistent.cm_translate_bilingual = True
    if persistent.cm_translation_cache is None:
        persistent.cm_translation_cache = {}
    if persistent.cm_frozen_vars is None:
        persistent.cm_frozen_vars = {}
    if persistent.cm_pinned_vars is None:
        persistent.cm_pinned_vars = []
    if getattr(persistent, 'cm_speed_level', None) is None:
        persistent.cm_speed_level = 1.0
    if getattr(persistent, 'cm_ui_scale_user', None) is None:
        persistent.cm_ui_scale_user = 1.0
    if getattr(persistent, 'cm_wheel_fix_mode', None) is None:
        persistent.cm_wheel_fix_mode = 'off'
    if getattr(persistent, 'cm_disable_rollback', None) is None:
        persistent.cm_disable_rollback = False
    if getattr(persistent, 'cm_single_key_shortcuts', None) is None:
        persistent.cm_single_key_shortcuts = True
    if getattr(persistent, 'cm_auto_recover_crash', None) is None:
        persistent.cm_auto_recover_crash = True
    if getattr(persistent, 'cm_language', None) is None:
        persistent.cm_language = 'en'

    # --------------------------------------------------------------------------
    # 2.1. HỆ THỐNG ĐA NGÔN NGỮ (LOCALIZATION ENGINE: EN / VI)
    # --------------------------------------------------------------------------
    CHEAT_LANGUAGES = [
        ('en', 'English', 'EN'),
        ('vi', u'Tiếng Việt', 'VI'),
    ]

    CHEAT_STRINGS = {
        'en': {
            'title': 'CHEAT ENGINE & HIDESKIP PRO 3.1',
            'ui_size': 'UI Scale:',
            'close': 'X CLOSE',
            'language': 'Language',
            'select_language': 'Select Interface Language',
            'save': 'Save',
            'cancel': 'Cancel',
            'refresh': u'🔄 Refresh',
            'clear': 'Clear',
            'locked': 'LOCKED',
            'lock': 'Lock',
            'tab_vars': 'Variables (Vars)',
            'tab_labels': 'Jump Scene (Labels)',
            'tab_unlocks': 'Unlocks & System',
            'tab_translate': 'AI Translate (AI_trans_pry)',
            'tab_help': 'Hotkeys & Help',
            'novel_controls': 'NOVEL CONTROLS',
            'hide_ui': 'Hide (H)',
            'skip': 'Skip (S)',
            'auto': 'Auto (A)',
            'log': 'Log (L)',
            'game_data': 'GAME DATA',
            'q_save': 'Q.Save',
            'q_load': 'Q.Load',
            'cheat_engine': 'CHEAT ENGINE',
            'cheat_menu_btn': 'Cheat Menu',
            'ai_trans_on': 'AI Trans: ON',
            'ai_trans_off': 'AI Trans: OFF',
            'wheel_log': 'Wheel: Open Log (Safe)',
            'wheel_lock': 'Wheel: Lock Rollback',
            'wheel_default': 'Wheel: Game Default',
            'filter': 'Filter:',
            'filter_all': 'All',
            'filter_num': 'Stats (Num)',
            'filter_bool': 'Flags (Bool)',
            'filter_str': 'Strings (Str)',
            'step_val': 'Step:',
            'search_var': 'Search stats/vars:',
            'search_label': 'Search:',
            'editing_num': 'Editing number...',
            'no_vars_found': 'No matching game variables found.',
            'empty_str': '(Empty / "")',
            'bool_true': 'ON (True)',
            'bool_false': 'OFF (False)',
            'edit_str': 'Edit Text',
            'clear_str': 'Clear',
            'game_object': '(Game Object)',
            'total_vars': 'Total: %d variables',
            'page_prev': '< Previous',
            'page_next': 'Next >',
            'page_info_vars': 'Page %d / %d (Total %d vars)',
            'search_scene': 'Search scenes (Labels):',
            'total_labels': 'Total: %d labels',
            'no_labels_found': 'No matching scenes (labels) found.',
            'jump_btn': '> Jump',
            'call_btn': '> Call',
            'page_info_labels': 'Page %d / %d (Total %d labels)',
            'lang_section_title': 'Cheat Menu Language',
            'lang_section_desc': 'Choose your preferred language for the Cheat Menu interface. Changes apply immediately.',
            'gallery_title': 'Unlock All CG & Gallery',
            'gallery_desc': 'Automatically unlock all CG images, scenes, and persistent Gallery/Replay flags.',
            'gallery_btn': 'UNLOCK ALL GALLERY & CG NOW',
            'dev_title': 'Developer Console Mode',
            'dev_desc': "Unlock Shift + O shortcut to open Ren'Py native Python interactive console.",
            'dev_active': 'Status: ACTIVE',
            'dev_inactive': 'Status: INACTIVE',
            'dev_btn': 'Enable Developer Mode',
            'skip_title': 'Force Skip Unseen Text',
            'skip_desc': 'Allow fast-forwarding through all dialogue, including unread/unseen text without stopping.',
            'skip_btn': 'Enable Permanent Force Skip',
            'wheel_title': 'Mouse Wheel Protection & Anti-Crash (Rollback Fix)',
            'wheel_desc': 'Eliminate crash/exception errors caused by broken Rollback when scrolling backward.',
            'wheel_mode': 'Wheel Mode:',
            'wheel_active_log': 'ACTIVE: Open Dialogue History (Safe, No Rollback)',
            'wheel_active_lock': 'ACTIVE: Lock Mouse Wheel (Completely Disabled)',
            'wheel_active_off': 'OFF: Game Default',
            'wheel_opt1': '1. Open Dialogue History (Recommended)',
            'wheel_opt2': '2. Lock Mouse Wheel',
            'wheel_opt3': '3. Restore Default',
            'rollback_lock_label': 'System-wide Rollback Lock:',
            'rollback_locked': 'LOCKED (Full Protection)',
            'rollback_unlocked': 'Unlocked (Normal)',
            'single_key_label': 'Single-key shortcuts H, S, A, L (Turn off if game uses WASD):',
            'single_key_on': 'Enabled (H, S, A, L)',
            'single_key_off': 'Disabled (Game keys prioritized)',
            'recovery_title': 'Auto-Crash Recovery & Interceptor',
            'recovery_desc': 'When script/variable errors occur: automatically log errors, auto-fix missing variables, and allow the game to continue without crashing.',
            'recovery_status_on': 'Status: AUTO PROTECTION ENABLED',
            'recovery_status_off': 'Status: PROTECTION DISABLED',
            'recovery_btn_on': 'ON (Recommended)',
            'recovery_btn_off': 'OFF',
            'sync_games_title': "Sync Cheat Menu to All Ren'Py Games (1-Click Sync)",
            'sync_games_desc': "Automatically scan and update the latest cheat_menu.rpy to other games in seconds.",
            'sync_games_btn': u'⚡ SYNC TO ALL GAMES NOW',
            'trans_not_active': '(!) TRANSLATION MODULE NOT ACTIVATED',
            'trans_info1': "Translation mechanism is located in the companion module: 'cheat_translate.rpy'.",
            'trans_info2': "The Cheat Menu shares interface with 'cheat_translate.rpy' and 'AI_trans_pry'.",
            'trans_guide_title': '(Guide) How to activate:',
            'trans_guide1': "1. Ensure 'cheat_translate.rpy' is placed in the game directory alongside 'cheat_menu.rpy'.",
            'trans_guide2': "2. Ensure 'AI_trans_pry' folder is present in the game directory.",
            'trans_guide3': '3. Restart the game to automatically enable translation features!',
            'hotkeys_title': 'KEYBOARD SHORTCUTS (HOTKEYS):',
            'hk_menu_key': u'• Keys [[Tab] / [[F1] / [[~] / [[Shift + C]',
            'hk_menu_desc': ': Open / Close Main Cheat Dashboard',
            'hk_star_key': u'• Key [[*] (Numpad Asterisk)',
            'hk_star_desc': ': Collapse / Expand Floating Sidebar',
            'hk_alt_star_key': u'• Keys [[Alt + *]',
            'hk_alt_star_desc': ': Show / Hide Floating Sidebar completely',
            'hk_h_key': u'• Key [[H]',
            'hk_h_desc': ': Hide UI to view full CG / background',
            'hk_s_key': u'• Key [[S]',
            'hk_s_desc': ': Toggle Force Skip (fast forward all text)',
            'hk_a_key': u'• Key [[A]',
            'hk_a_desc': ': Toggle Auto-Forward text mode',
            'hk_l_key': u'• Key [[L]',
            'hk_l_desc': ': Open Dialogue History & Restore Points',
            'hk_dev_key': u'• Keys [[Shift + O]',
            'hk_dev_desc': ": Open Ren'Py native Python console",
            'hk_cloud_key': u'• Keys [[Shift + F11] / [[Shift + F10]',
            'hk_cloud_desc': ': GitHub Auto-Repair & Update / Clean Cache',
            'hk_wheel_key': u'• Mouse Wheel (Scroll Up)',
            'hk_wheel_desc': ': Anti-crash Rollback (Open History / Lock Rollback)',
            'scaling_title': 'UI AUTO-SCALING & DISPLAY PRESETS:',
            'game_res': '(Game Resolution: %s)',
            'scaling_desc': 'Cheat Menu automatically adapts to your game resolution. Select a scale preset:',
            'tip_pinned': '(Tip) Click (*) to pin important variables to top. Click LOCK to freeze values!',
            'hist_title': 'DIALOGUE HISTORY & RESTORE POINTS (HISTORY LOG)',
            'hist_count': '(%d dialogue lines)',
            'hist_desc': 'Click directly on any dialogue line or the Restore button to jump back to that point.',
            'hist_empty_title': 'No dialogue history recorded yet.',
            'hist_empty_desc': 'Play through a few dialogue lines and reopen this screen!',
            'hist_restore': '< Jump Here',
            'hist_footer_tip': 'Tip: Scroll mouse wheel to navigate | Click any line to jump back.',
            'hist_open_game': 'Open Native Game History',
            'notify_refresh': 'Refreshed data from save game!',
            'notify_rollback_history': 'Enabled: Mouse wheel opens Dialogue History (Anti-crash Rollback)!',
            'notify_rollback_locked': 'Enabled: Mouse wheel locked & Rollback disabled!',
            'notify_rollback_default': 'Protection disabled: Mouse wheel restored to game default!',
            'notify_rollback_hard_lock': 'Game Rollback has been LOCKED (Crash protection)!',
            'notify_rollback_hard_unlock': 'Game Rollback has been UNLOCKED!',
            'notify_max_clamp': 'Value exceeded limit! Clamped to max: %s',
            'notify_invalid_number': 'Invalid number format! Please enter valid digits.',
            'notify_gallery_unlocked': 'Safely unlocked all CGs, Gallery & Music!',
            'notify_force_skip_on': 'Permanent Force Skip enabled!',
            'notify_need_game_jump': 'Please start New Game or Load a Save before jumping scenes!',
            'notify_jump_failed': 'Cannot jump to this label: %s',
            'notify_need_game_call': 'Please start New Game or Load a Save before calling scenes!',
            'notify_sync_src_not_found': 'Source cheat_menu.rpy file not found for sync!',
            'notify_sync_dir_not_found': 'Directory not found: %s',
            'notify_sync_done': 'Synced cheat_menu.rpy to %d game directories!',
            'notify_rollback_only_in_game': 'Can only jump back while in an active game session!',
            'notify_rollback_success': 'Jumped back to selected dialogue!',
            'notify_rollback_too_far': 'Cannot jump back to this point (too far or no checkpoint recorded).',
            'notify_rollback_error': 'Error: Game encountered memory error during Rollback!',
            'notify_lang_changed': 'Language changed to English!',
            'notify_export_merged': 'This feature has been merged into the Translate Game (xlsx) button!',
            'notify_error_prefix': 'Error: %s',
            'notify_call_failed': 'Cannot call this label: %s',
            'notify_clamped_game_max': 'Set to valid game maximum (%s) based on game data!',
            'notify_max_value_set': 'Maximized value to (%s)!',
            'notify_crash_intercepted': u'⚡ Cheat Menu: Auto-intercepted error: %s',
            'notify_sync_error': 'Sync error: %s',
            'notify_master_updated': u'⚡ [Cheat Menu] Auto-updated and loaded latest version from Master!',
        },
        'vi': {
            'title': 'CHEAT ENGINE & HIDESKIP PRO 3.1',
            'ui_size': u'Kích cỡ UI:',
            'close': u'X ĐÓNG',
            'language': u'Ngôn ngữ',
            'select_language': u'Chọn Ngôn Ngữ Giao Diện',
            'save': u'Lưu',
            'cancel': u'Hủy',
            'refresh': u'🔄 Làm mới',
            'clear': u'Xóa',
            'locked': u'KHÓA',
            'lock': u'Khóa',
            'tab_vars': u'Quản lý Biến (Vars)',
            'tab_labels': u'Nhảy cảnh (Labels)',
            'tab_unlocks': u'Mở khóa & Hệ thống',
            'tab_translate': u'AI Dịch thuật (AI_trans_pry)',
            'tab_help': u'Phím tắt & Trợ giúp',
            'novel_controls': 'NOVEL CONTROLS',
            'hide_ui': 'Hide (H)',
            'skip': 'Skip (S)',
            'auto': 'Auto (A)',
            'log': 'Log (L)',
            'game_data': 'GAME DATA',
            'q_save': 'Q.Save',
            'q_load': 'Q.Load',
            'cheat_engine': 'CHEAT ENGINE',
            'cheat_menu_btn': 'Cheat Menu',
            'ai_trans_on': u'Dịch AI: BẬT',
            'ai_trans_off': u'Dịch AI: TẮT',
            'wheel_log': u'Lăn chuột: Mở Log (An toàn)',
            'wheel_lock': u'Lăn chuột: Khóa Rollback',
            'wheel_default': u'Lăn chuột: Mặc định game',
            'filter': u'Lọc:',
            'filter_all': u'Tất cả',
            'filter_num': u'Số (Stats)',
            'filter_bool': u'Cờ (Bool)',
            'filter_str': u'Chữ (Str)',
            'step_val': u'Bước nhảy:',
            'search_var': u'Tìm chỉ số/biến:',
            'search_label': u'Tìm:',
            'editing_num': u'Đang sửa số...',
            'no_vars_found': u'Không tìm thấy biến game nào phù hợp với bộ lọc.',
            'empty_str': u'(Trống / "")',
            'bool_true': u'BẬT (True)',
            'bool_false': u'TẮT (False)',
            'edit_str': u'Sửa chữ',
            'clear_str': u'Xóa rỗng',
            'game_object': u'(Đối tượng game)',
            'total_vars': u'Tổng: %d biến',
            'page_prev': u'< Trang trước',
            'page_next': u'Trang sau >',
            'page_info_vars': u'Trang %d / %d (Tổng %d biến)',
            'search_scene': u'Tìm kiếm cảnh (Label):',
            'total_labels': u'Tổng: %d labels',
            'no_labels_found': u'Không tìm thấy cảnh (label) nào phù hợp.',
            'jump_btn': u'> Nhảy tới (Jump)',
            'call_btn': u'> Gọi cảnh (Call)',
            'page_info_labels': u'Trang %d / %d (Tổng %d labels)',
            'lang_section_title': u'Ngôn ngữ Cheat Menu',
            'lang_section_desc': u'Chọn ngôn ngữ hiển thị cho giao diện Cheat Menu. Cài đặt có hiệu lực ngay lập tức.',
            'gallery_title': u'Mở khóa toàn bộ Thư viện ảnh (Gallery & CG)',
            'gallery_desc': u'Tự động kích hoạt toàn bộ hình ảnh và cờ persistent lưu trữ Gallery/Replay.',
            'gallery_btn': u'KÍCH HOẠT MỞ KHÓA TOÀN BỘ GALLERY',
            'dev_title': u'Chế độ Nhà phát triển (Developer Console)',
            'dev_desc': u"Mở khóa phím tắt Shift + O để bật Console gõ lệnh Python trực tiếp của Ren'Py.",
            'dev_active': u'Trạng thái: ĐÃ KÍCH HOẠT',
            'dev_inactive': u'Trạng thái: CHƯA KÍCH HOẠT',
            'dev_btn': u'Bật Developer Mode',
            'skip_title': u'Bỏ qua không giới hạn (Force Skip Unseen Text)',
            'skip_desc': u'Cho phép Skip tua nhanh qua cả những đoạn thoại chưa từng xem qua trước đây mà không bị dừng.',
            'skip_btn': u'Kích hoạt Force Skip Vĩnh Viễn',
            'wheel_title': u'Bảo vệ con lăn chuột & Chống lỗi tua ngược (Rollback Fix)',
            'wheel_desc': u'Khắc phục triệt để lỗi Crash / Exception ở các game bị hỏng tính năng Rollback khi lăn chuột ngược lại.',
            'wheel_mode': u'Chế độ con lăn:',
            'wheel_active_log': u'ĐANG BẬT: Mở Lịch sử thoại (Xem lại thoại an toàn, không Rollback)',
            'wheel_active_lock': u'ĐANG BẬT: Khóa con lăn chuột (Vô hiệu hóa hoàn toàn)',
            'wheel_active_off': u'ĐANG TẮT: Mặc định gốc của game',
            'wheel_opt1': u'1. Mở Lịch Sử Thoại (Khuyên Dùng)',
            'wheel_opt2': u'2. Khóa Con Lăn Chuột',
            'wheel_opt3': u'3. Khôi Phục Mặc Định',
            'rollback_lock_label': u'Khóa Rollback toàn hệ thống:',
            'rollback_locked': u'ĐANG KHÓA (Bảo vệ tuyệt đối)',
            'rollback_unlocked': u'Đang mở (Bình thường)',
            'single_key_label': u'Phím tắt đơn H, S, A, L (Tắt nếu game dùng WASD):',
            'single_key_on': u'Đang Bật (H, S, A, L)',
            'single_key_off': u'Đã Tắt (Ưu tiên phím game)',
            'recovery_title': u'Tự động cứu hộ & Chống sập game khi gặp lỗi (Auto-Crash Recovery)',
            'recovery_desc': u'Khi game xảy ra lỗi kịch bản / tràn biến: Tự động ghi lại lỗi vào cheat_crash_log.txt, tự sửa biến và cho phép game tiếp tục chạy thay vì văng sập ra Desktop.',
            'recovery_status_on': u'Trạng thái: ĐANG BẬT BẢO VỆ TỰ ĐỘNG',
            'recovery_status_off': u'Trạng thái: ĐÃ TẮT BẢO VỆ',
            'recovery_btn_on': u'BẬT (Khuyên dùng)',
            'recovery_btn_off': u'TẮT',
            'sync_games_title': u"Đồng bộ Cheat Menu sang tất cả game Ren'Py (1-Click Multi-Game Sync)",
            'sync_games_desc': u'Tự động quét toàn bộ thư mục và cập nhật bản cheat_menu.rpy mới nhất này sang tất cả các game khác chỉ trong 1 giây.',
            'sync_games_btn': u'⚡ KÍCH HOẠT ĐỒNG BỘ CHO TẤT CẢ CÁC GAME NGAY',
            'trans_not_active': u'(!) CHƯA KÍCH HOẠT MODULE DỊCH THUẬT',
            'trans_info1': u"Cơ chế dịch thuật đã được tách thành module độc lập: 'cheat_translate.rpy'.",
            'trans_info2': u"Theo thiết kế mới, Cheat Menu dùng chung menu phiên dịch với 'cheat_translate.rpy' và 'AI_trans_pry'.",
            'trans_guide_title': u'(Hướng dẫn) Cách kích hoạt:',
            'trans_guide1': u"1. Đảm bảo file 'cheat_translate.rpy' nằm cùng thư mục game với 'cheat_menu.rpy'.",
            'trans_guide2': u"2. Đảm bảo thư mục 'AI_trans_pry' nằm trong thư mục game.",
            'trans_guide3': u'3. Khởi động lại game, Cheat Menu sẽ tự động phát hiện và mở khóa toàn bộ tính năng dịch thuật!',
            'hotkeys_title': u'DANH SÁCH PHÍM TẮT TIỆN LỢI (HOTKEYS):',
            'hk_menu_key': u'• Phím [[Tab] / [[F1] / [[~] / [[Shift + C]',
            'hk_menu_desc': u': Mở / Đóng Bảng điều khiển Cheat chính',
            'hk_star_key': u'• Phím [[*] (Phím sao Numpad)',
            'hk_star_desc': u': Thu gọn / Mở rộng Thanh nổi bên phải',
            'hk_alt_star_key': u'• Phím [[Alt + *]',
            'hk_alt_star_desc': u': Bật / Tắt ẩn hoàn toàn Thanh nổi bên phải',
            'hk_h_key': u'• Phím [[H]',
            'hk_h_desc': u': Ẩn khung thoại (Hide UI) để xem trọn vẹn CG / hình nền',
            'hk_s_key': u'• Phím [[S]',
            'hk_s_desc': u': Bật / Tắt Tua nhanh (Tua qua tất cả hội thoại, kể cả chưa đọc)',
            'hk_a_key': u'• Phím [[A]',
            'hk_a_desc': u': Bật / Tắt chế độ Tự động đọc thoại (Auto-Forward)',
            'hk_l_key': u'• Phím [[L]',
            'hk_l_desc': u': Mở Nhật ký thoại & Điểm quay lại (History Log)',
            'hk_dev_key': u'• Phím [[Shift + O]',
            'hk_dev_desc': u": Mở Console dòng lệnh Python gốc của Ren'Py",
            'hk_cloud_key': u'• Phím [[Shift + F11] / [[Shift + F10]',
            'hk_cloud_desc': u': Tải bản mới từ GitHub Cloud / Dọn sạch Cache Bytecode',
            'hk_wheel_key': u'• Con lăn chuột (Lăn lên)',
            'hk_wheel_desc': u': Chống lỗi Rollback (Tùy chọn: Mở Lịch sử thoại / Khóa Rollback)',
            'scaling_title': u'ĐỒNG BỘ KÍCH CỠ GIAO DIỆN (AUTO-SCALING & UI SCALE):',
            'game_res': u'(Độ phân giải game: %s)',
            'scaling_desc': u'Cheat Menu tự động nhận diện độ phân giải game và scale tỷ lệ chuẩn (100% không can thiệp hay thay đổi cấu hình gốc của game). Bạn có thể chọn nhanh kích cỡ mong muốn:',
            'tip_pinned': u'(Mẹo) Bấm vào nút (*) để ghim biến quan trọng lên đầu. Bấm vào nút KHÓA để đóng băng giá trị không bao giờ bị giảm!',
            'hist_title': u'NHẬT KÝ HỘI THOẠI & ĐIỂM QUAY LẠI (HISTORY LOG)',
            'hist_count': u'(%d câu thoại)',
            'hist_desc': u'Bấm trực tiếp vào câu thoại hoặc nút Quay lại để nhảy ngược game về thời điểm đó.',
            'hist_empty_title': u'Chưa có dữ liệu lịch sử hội thoại nào được ghi lại.',
            'hist_empty_desc': u'Hãy tiếp tục chơi qua vài câu thoại rồi mở lại bảng này nhé!',
            'hist_restore': u'< Quay lại',
            'hist_footer_tip': u'Mẹo: Lăn chuột để cuộn danh sách | Bấm vào bất kỳ câu nào để quay lại.',
            'hist_open_game': u'Mở History gốc của game',
            'notify_refresh': u'Đã làm mới dữ liệu từ file save!',
            'notify_rollback_history': u'Đã bật: Lăn chuột chuyển sang mở Lịch sử thoại (Chống lỗi Rollback)!',
            'notify_rollback_locked': u'Đã bật: Khóa con lăn chuột & vô hiệu hóa Rollback hoàn toàn!',
            'notify_rollback_default': u'Đã tắt bảo vệ: Con lăn chuột về mặc định của game!',
            'notify_rollback_hard_lock': u'Đã KHÓA hoàn toàn Rollback của game (Chống crash)!',
            'notify_rollback_hard_unlock': u'Đã MỞ LẠI Rollback của game!',
            'notify_max_clamp': u'Giá trị vượt giới hạn! Tự động đưa về mức tối đa: %s',
            'notify_invalid_number': u'Giá trị số không hợp lệ! Vui lòng chỉ nhập số.',
            'notify_gallery_unlocked': u'Đã mở khóa toàn bộ CG, Gallery & Âm nhạc an toàn!',
            'notify_force_skip_on': u'Đã bật Force Skip vĩnh viễn!',
            'notify_need_game_jump': u'Vui lòng Bắt đầu game (New Game) hoặc Load Save trước khi Nhảy cảnh!',
            'notify_jump_failed': u'Không thể nhảy tới cảnh này: %s',
            'notify_need_game_call': u'Vui lòng Bắt đầu game (New Game) hoặc Load Save trước khi Gọi cảnh!',
            'notify_sync_src_not_found': u'Không tìm thấy file nguồn cheat_menu.rpy để đồng bộ!',
            'notify_sync_dir_not_found': u'Không tìm thấy thư mục: %s',
            'notify_sync_done': u'Đã đồng bộ Cheat Menu mới nhất cho %d thư mục game!',
            'notify_rollback_only_in_game': u'Chỉ có thể quay lại khi đang trong tiến trình game!',
            'notify_rollback_success': u'Đã quay lại đoạn hội thoại đã chọn!',
            'notify_rollback_too_far': u'Không thể quay lại điểm này (Điểm này quá xa hoặc game không lưu checkpoint).',
            'notify_rollback_error': u'Lỗi: Game này gặp sự cố bộ nhớ khi Rollback!',
            'notify_lang_changed': u'Đã chuyển ngôn ngữ sang Tiếng Việt!',
            'notify_export_merged': u'Tính năng này đã được gộp vào nút Dịch Game (xlsx)!',
            'notify_error_prefix': u'Lỗi: %s',
            'notify_call_failed': u'Không thể gọi cảnh này: %s',
            'notify_clamped_game_max': u'Đã đặt giá trị tối đa hợp lệ (%s) theo dữ liệu của game!',
            'notify_max_value_set': u'Đã nâng giá trị lên tối đa (%s)!',
            'notify_crash_intercepted': u'⚡ Cheat Menu: Đã tự động bắt và chặn lỗi: %s',
            'notify_sync_error': u'Lỗi đồng bộ: %s',
            'notify_master_updated': u'⚡ [Cheat Menu] Đã tự động cập nhật và nạp bản mới nhất từ Master!',
        }
    }

    def cheat_get_lang():
        lang = getattr(persistent, 'cm_language', None)
        if not lang or lang not in CHEAT_STRINGS:
            return 'en'
        return lang

    def cheat_set_lang(lang):
        if lang in CHEAT_STRINGS:
            persistent.cm_language = lang
            cheat_notify('notify_lang_changed')
            try:
                renpy.restart_interaction()
            except Exception:
                pass

    def cheat_tr(key, *args):
        lang = cheat_get_lang()
        text = CHEAT_STRINGS.get(lang, {}).get(key)
        if text is None:
            text = CHEAT_STRINGS.get('en', {}).get(key, key)
        if args:
            try:
                return text % args
            except Exception:
                return text
        return text

    renpy.store.cheat_tr = cheat_tr
    renpy.store._cm_t = cheat_tr

    _prev_rollback_state = True
    _orig_rollback_keys = None

    def cheat_notify(msg, *args):
        """Bọc thông báo an toàn, tự động dịch thông báo theo ngôn ngữ đang chọn."""
        try:
            if hasattr(renpy, 'game') and hasattr(renpy.game, 'context'):
                ctx = renpy.game.context()
                if getattr(ctx, 'init_phase', False):
                    return
            trans_text = cheat_tr(msg, *args) if isinstance(msg, _STR_TYPES) and msg in CHEAT_STRINGS.get('en', {}) else msg
            if args and trans_text == msg:
                try:
                    trans_text = msg % args
                except Exception:
                    pass
            renpy.notify(trans_text)
        except Exception:
            pass

    def cheat_dummy_func():
        """Hàm rỗng dùng để nuốt sự kiện lăn chuột khi khóa Rollback."""
        pass

    def cheat_get_history_entries():
        """Lấy danh sách các câu thoại trong lịch sử của game."""
        try:
            h_list = getattr(renpy.store, '_history_list', None)
            if h_list and isinstance(h_list, (list, tuple)):
                return list(h_list)
        except Exception:
            pass
        return []

    def cheat_rollback_to_history(h_entry, steps=None):
        """
        Quay lại điểm hội thoại được chọn trong lịch sử.
        Bảo vệ an toàn chống crash nếu game bị lỗi Rollback.
        """
        try:
            if not cheat_can_jump_safely():
                cheat_notify('notify_rollback_only_in_game')
                return

            # Tạm thời bật rollback_enabled để engine cho phép tua lại
            _safe_set_config('rollback_enabled', True)

            success = False
            rb_id = getattr(h_entry, 'rollback_identifier', None)

            # 1. Thử dùng RollbackToIdentifier (chuẩn Ren'Py 7.4+)
            if rb_id is not None:
                try:
                    if hasattr(renpy.exports, 'RollbackToIdentifier'):
                        act = renpy.exports.RollbackToIdentifier(rb_id)
                        renpy.hide_screen('cheat_history_modal')
                        renpy.run(act)
                        cheat_notify('notify_rollback_success')
                        return
                    elif hasattr(renpy, 'rollback'):
                        res = renpy.rollback(force=True, rollback_identifier=rb_id)
                        if res:
                            success = True
                except Exception:
                    success = False

            # 2. Fallback dùng số bước checkpoint nếu identifier không thành công
            if not success and steps is not None and steps > 0:
                try:
                    res = renpy.rollback(force=True, checkpoints=steps)
                    if res:
                        success = True
                except Exception:
                    success = False

            if success:
                renpy.hide_screen('cheat_history_modal')
                cheat_notify('notify_rollback_success')
                renpy.restart_interaction()
            else:
                cheat_notify('notify_rollback_too_far')
        except Exception as e:
            cheat_notify('notify_rollback_error')
        finally:
            if getattr(persistent, 'cm_disable_rollback', False) or getattr(persistent, 'cm_wheel_fix_mode', 'off') == 'disable':
                _safe_set_config('rollback_enabled', False)

    def cheat_safe_show_history():
        """Mở an toàn màn hình Lịch sử hội thoại (History Log)."""
        try:
            renpy.show_screen('cheat_history_modal')
            renpy.restart_interaction()
        except Exception:
            try:
                for s in ('history', 'text_history', 'log'):
                    if renpy.has_screen(s):
                        renpy.show_screen(s)
                        renpy.restart_interaction()
                        return
                renpy.run(ShowMenu("history"))
            except Exception:
                pass

    def cheat_apply_wheel_protection():
        """Áp dụng cấu hình bảo vệ con lăn chuột chống crash Rollback."""
        global _orig_rollback_keys
        mode = getattr(persistent, 'cm_wheel_fix_mode', 'off')

        try:
            km = getattr(renpy.config, 'keymap', None)
            if km and isinstance(km, dict) and 'rollback' in km:
                if _orig_rollback_keys is None:
                    _orig_rollback_keys = list(km['rollback'])

                if mode in ('history', 'disable'):
                    km['rollback'] = [k for k in _orig_rollback_keys if k not in ('mousedown_4', 'wheelup', 'btn_dp_up')]
                else:
                    km['rollback'] = list(_orig_rollback_keys)
        except Exception:
            pass

        if getattr(persistent, 'cm_disable_rollback', False) or mode == 'disable':
            _safe_set_config('rollback_enabled', False)
        else:
            _safe_set_config('rollback_enabled', True)

        # Làm sạch các Keymap trong config.underlay để không bao giờ chứa module object
        try:
            import types
            for u in getattr(renpy.config, 'underlay', []):
                km = getattr(u, 'keymap', None)
                if isinstance(km, dict) and 'rollback' in km:
                    _target_rb = km['rollback']
                    if not callable(_target_rb) or (hasattr(types, 'ModuleType') and isinstance(_target_rb, types.ModuleType)):
                        km['rollback'] = getattr(renpy.exports, 'rollback', renpy.rollback)
        except Exception:
            pass

        # Đảm bảo hard_rollback_limit luôn là số nguyên (int), không bao giờ là None
        try:
            hrl = getattr(renpy.config, 'hard_rollback_limit', None)
            if hrl is None or not isinstance(hrl, int) or hrl < 1:
                renpy.config.hard_rollback_limit = 100
        except Exception:
            pass

    def cheat_set_wheel_fix_mode(mode):
        """Thiết lập chế độ con lăn chuột: 'history', 'disable', 'off'."""
        persistent.cm_wheel_fix_mode = mode
        cheat_apply_wheel_protection()
        if mode == 'history':
            cheat_notify('notify_rollback_history')
        elif mode == 'disable':
            cheat_notify('notify_rollback_locked')
        else:
            cheat_notify('notify_rollback_default')
        renpy.restart_interaction()

    def cheat_cycle_wheel_fix_mode():
        """Chuyển đổi luân phiên: off -> history -> disable -> off."""
        curr = getattr(persistent, 'cm_wheel_fix_mode', 'off')
        if curr == 'off':
            cheat_set_wheel_fix_mode('history')
        elif curr == 'history':
            cheat_set_wheel_fix_mode('disable')
        else:
            cheat_set_wheel_fix_mode('off')

    def cheat_toggle_disable_rollback():
        """Bật/tắt khóa Rollback Engine toàn hệ thống."""
        curr = getattr(persistent, 'cm_disable_rollback', False)
        persistent.cm_disable_rollback = not curr
        cheat_apply_wheel_protection()
        if persistent.cm_disable_rollback:
            cheat_notify('notify_rollback_hard_lock')
        else:
            cheat_notify('notify_rollback_hard_unlock')
        renpy.restart_interaction()

    def cheat_modal_on_show():
        global _prev_rollback_state
        _prev_rollback_state = getattr(config, 'rollback_enabled', True)
        _safe_set_config('rollback_enabled', False)
        cheat_setup_isolated_styles()
        cheat_menu_state.invalidate_cache(False)

    def cheat_modal_on_hide():
        global _prev_rollback_state
        if getattr(persistent, 'cm_disable_rollback', False) or getattr(persistent, 'cm_wheel_fix_mode', 'off') == 'disable':
            _safe_set_config('rollback_enabled', False)
        else:
            _safe_set_config('rollback_enabled', _prev_rollback_state)

    def cheat_get_ui_scale():
        """
        Tính toán hệ số zoom tự động dựa trên độ phân giải ảo của game.
        Đảm bảo Cheat Menu hiển thị với kích thước và tỉ lệ màn hình
        đồng nhất 100% trên mọi game (720p, 1080p, 2K, 4K, 800x600...).
        Tự động giới hạn để không bao giờ tràn/cắt lọt ra ngoài mép màn hình.
        """
        try:
            sw = float(getattr(config, 'screen_width', 1280) or 1280)
            sh = float(getattr(config, 'screen_height', 720) or 720)
            base_scale = min(sw / 1280.0, sh / 720.0)
            user_mult = float(getattr(persistent, 'cm_ui_scale_user', 1.0) or 1.0)
            target = base_scale * user_mult
            # Giới hạn scale tối đa để không bao giờ bị cắt mất phần dưới trên màn 720p (khung cao 640px)
            max_scale = (sh * 0.96) / 640.0
            return max(0.4, min(max_scale, target))
        except Exception:
            return 1.0

    def cheat_get_bar_y():
        """Tính toán vị trí Y của thanh công cụ nổi theo tỷ lệ màn hình game."""
        try:
            y_base = getattr(persistent, 'cm_bar_y', 140)
            if y_base is None or y_base < 10 or y_base > 600:
                y_base = 140
            sw = float(getattr(config, 'screen_width', 1280) or 1280)
            sh = float(getattr(config, 'screen_height', 720) or 720)
            base_scale = min(sw / 1280.0, sh / 720.0)
            actual_y = int(y_base * base_scale)
            return max(5, min(int(sh - 120), actual_y))
        except Exception:
            return 140

    def cheat_step_ui_scale(delta):
        curr = float(getattr(persistent, 'cm_ui_scale_user', 1.0) or 1.0)
        new_val = max(0.7, min(1.6, round((curr + delta) * 10) / 10.0))
        persistent.cm_ui_scale_user = new_val
        renpy.restart_interaction()

    def cheat_set_ui_scale(val):
        persistent.cm_ui_scale_user = max(0.7, min(1.6, float(val)))
        renpy.restart_interaction()

    # Ép Ren'Py cho phép bỏ qua cả câu thoại chưa từng đọc (An toàn mọi bản)
    _safe_set_pref('skip_unseen', True)
    _safe_set_config('allow_skipping', True)
    _safe_set_config('fast_skipping', True)
    _safe_set_config('history_length', 500)
    _safe_set_config('history_current_dialogue', True)

    # Khắc phục triệt để lỗi TypeError '<' not supported between instances of 'int' and 'NoneType'
    try:
        _hrl = getattr(renpy.config, 'hard_rollback_limit', None)
        if _hrl is None or not isinstance(_hrl, int) or _hrl < 1:
            renpy.config.hard_rollback_limit = 100
    except Exception:
        pass

    # --------------------------------------------------------------------------
    # 3. HÀM FORCE SKIP TOÀN DIỆN (TUA QUA TẤT CẢ CÁC CÂU THOẠI)
    # --------------------------------------------------------------------------
    def cheat_toggle_force_skip():
        """Bật/tắt chế độ tua nhanh toàn bộ hội thoại (kể cả câu thoại chưa từng đọc)."""
        _safe_set_pref('skip_unseen', True)
        _safe_set_config('allow_skipping', True)

        try:
            curr_skip = getattr(renpy.config, 'skipping', None)
            if curr_skip:
                renpy.config.skipping = None
            else:
                renpy.config.skipping = "slow"
        except Exception:
            pass
        try:
            renpy.restart_interaction()
        except Exception:
            pass

    # --------------------------------------------------------------------------
    # 4. HỆ THỐNG LIÊN KẾT AI PHIÊN DỊCH (CHEAT_TRANSLATE & AI_TRANS_PRY BRIDGE)
    # --------------------------------------------------------------------------
    def cheat_has_ai_trans():
        """Kiểm tra xem module cheat_translate và engine AI có khả dụng không."""
        if getattr(renpy.store, 'cheat_trans_has_ai', None) and callable(renpy.store.cheat_trans_has_ai):
            return renpy.store.cheat_trans_has_ai()
        if getattr(renpy.store, 'ai_trans_available', False) and getattr(renpy.store, 'ai_trans_engine', None):
            return True
        return False

    def cheat_get_current_speaker():
        if getattr(renpy.store, 'cheat_trans_get_speaker', None) and callable(renpy.store.cheat_trans_get_speaker):
            return renpy.store.cheat_trans_get_speaker()
        try:
            who_obj = getattr(renpy.store, '_last_say_who', None)
            if who_obj:
                if isinstance(who_obj, (str, type(u""))):
                    return _safe_str(who_obj)
                name_attr = getattr(who_obj, 'name', None)
                if name_attr:
                    return _safe_str(name_attr)
        except Exception:
            pass
        return None


    # --------------------------------------------------------------------------
    # 5. HỆ THỐNG QUẢN LÝ BIẾN & ĐÓNG BĂNG (VARIABLE MANAGER & FREEZER)
    # --------------------------------------------------------------------------
    IGNORED_STORE_KEYS = {
        'renpy', 'config', 'gui', 'style', 'store', 'persistent', 'preferences',
        'build', 'theme', 'default', 'anim', 'achievement', 'im', 'ui', 'gl_test',
        'cheat_menu_state', 'ai_trans_engine', 'ai_trans_available', 'ai_trans_dir',
        'IGNORED_STORE_KEYS', 'PY3'
    }

    STAT_KEYWORD_SYNONYMS = {
        'tien': ('gold', 'money', 'cash', 'coin', 'coins', 'silver', 'credit', 'credits', 'gem', 'gems', 'rubies', 'diamond', 'currency'),
        'tiền': ('gold', 'money', 'cash', 'coin', 'coins', 'silver', 'credit', 'credits', 'gem', 'gems', 'rubies', 'diamond', 'currency'),
        'vang': ('gold', 'coin', 'coins'),
        'vàng': ('gold', 'coin', 'coins'),
        'mau': ('hp', 'health', 'life', 'vitality', 'hitpoint', 'max_hp'),
        'máu': ('hp', 'health', 'life', 'vitality', 'hitpoint', 'max_hp'),
        'hp': ('hp', 'health', 'life', 'vitality'),
        'mp': ('mp', 'mana', 'magic', 'sp'),
        'mana': ('mp', 'mana', 'magic'),
        'nang luong': ('energy', 'stamina', 'sp', 'mp', 'mana'),
        'năng lượng': ('energy', 'stamina', 'sp', 'mp', 'mana'),
        'the luc': ('stamina', 'energy', 'vitality', 'vit'),
        'thể lực': ('stamina', 'energy', 'vitality', 'vit'),
        'cap': ('level', 'lvl', 'rank', 'grade'),
        'cấp': ('level', 'lvl', 'rank', 'grade'),
        'level': ('level', 'lvl', 'rank', 'grade'),
        'diem': ('point', 'points', 'score', 'ap', 'sp', 'cp', 'lp', 'ep', 'dp', 'bonus'),
        'điểm': ('point', 'points', 'score', 'ap', 'sp', 'cp', 'lp', 'ep', 'dp', 'bonus'),
        'exp': ('exp', 'xp', 'experience'),
        'kinh nghiem': ('exp', 'xp', 'experience'),
        'kinh nghiệm': ('exp', 'xp', 'experience'),
        'suc manh': ('str', 'strength', 'power', 'atk', 'attack'),
        'sức mạnh': ('str', 'strength', 'power', 'atk', 'attack'),
        'str': ('str', 'strength', 'power'),
        'phong thu': ('def', 'defense', 'armor', 'shield'),
        'phòng thủ': ('def', 'defense', 'armor', 'shield'),
        'def': ('def', 'defense', 'armor', 'shield'),
        'nhanh nhen': ('agi', 'agility', 'speed', 'dex', 'dexterity'),
        'nhanh nhẹn': ('agi', 'agility', 'speed', 'dex', 'dexterity'),
        'agi': ('agi', 'agility', 'speed'),
        'thong minh': ('int', 'intelligence', 'wis', 'wisdom', 'mind'),
        'thông minh': ('int', 'intelligence', 'wis', 'wisdom', 'mind'),
        'int': ('int', 'intelligence', 'wis'),
        'may man': ('luk', 'luck', 'fortune'),
        'may mắn': ('luk', 'luck', 'fortune'),
        'luk': ('luk', 'luck', 'fortune'),
        'tinh cam': ('love', 'affection', 'affinity', 'relationship', 'favor', 'trust', 'heart', 'romance'),
        'tình cảm': ('love', 'affection', 'affinity', 'relationship', 'favor', 'trust', 'heart', 'romance'),
        'dam me': ('lust', 'desire', 'libido', 'arousal', 'horny', 'corruption'),
        'đam mê': ('lust', 'desire', 'libido', 'arousal', 'horny', 'corruption'),
        'tha hoa': ('corruption', 'corrupt', 'taint', 'darkness'),
        'tha hóa': ('corruption', 'corrupt', 'taint', 'darkness'),
        'thoi gian': ('time', 'day', 'hour', 'date', 'turn', 'month', 'year', 'period'),
        'thời gian': ('time', 'day', 'hour', 'date', 'turn', 'month', 'year', 'period'),
    }

    COMMON_STAT_PRIORITY = {
        'gold', 'money', 'cash', 'coin', 'coins', 'gem', 'gems', 'credits', 'silver',
        'hp', 'health', 'life', 'max_hp', 'mp', 'mana', 'magic', 'max_mp', 'energy', 'stamina',
        'level', 'lvl', 'exp', 'xp', 'points', 'point', 'skill_points', 'stat_points',
        'str', 'strength', 'atk', 'attack', 'def', 'defense', 'agi', 'agility', 'int', 'intelligence',
        'dex', 'dexterity', 'vit', 'vitality', 'luk', 'luck', 'speed', 'power',
        'love', 'affection', 'affinity', 'lust', 'corruption', 'karma', 'reputation',
        'day', 'hour', 'time', 'turn'
    }

    _STAT_PRIORITY_TOKENS = frozenset([
        'hp', 'mp', 'gold', 'money', 'exp', 'xp', 'str', 'lvl', 'point', 'points',
        'stat', 'stats', 'cash', 'coin', 'coins', 'gem', 'gems', 'atk', 'def', 'agi',
        'int', 'luk', 'dex', 'vit', 'energy', 'stamina', 'mana', 'health', 'love',
        'affection', 'affinity', 'lust', 'corruption', 'karma', 'reputation', 'score',
        'credit', 'credits', 'silver', 'rubies', 'diamond', 'day', 'hour', 'time', 'turn'
    ])

    def _cheat_is_common_stat(var_name):
        last_part = var_name.split('.')[-1].split("['")[-1].replace("']", "").lower()
        if last_part in COMMON_STAT_PRIORITY or last_part in _STAT_PRIORITY_TOKENS:
            return True
        words = set(re.findall(r'[a-zA-Z0-9]+', last_part))
        if words & _STAT_PRIORITY_TOKENS:
            return True
        return False

    _CHEAT_NOT_FOUND = object()

    def _cheat_tokenize_path(key):
        """
        Phân giải đường dẫn biến dạng chuỗi thành danh sách các bước truy xuất.
        Hỗ trợ:
          - mc.stats['gold'] -> [('attr', 'mc'), ('attr', 'stats'), ('item', 'gold')]
          - player.hp -> [('attr', 'player'), ('attr', 'hp')]
          - flags['met_alice'] -> [('attr', 'flags'), ('item', 'met_alice')]
          - inventory[0] -> [('attr', 'inventory'), ('item', 0)]
        """
        tokens = []
        i = 0
        n = len(key)
        while i < n and key[i] not in ('.', '['):
            i += 1
        first_ident = key[:i].strip()
        if not first_ident:
            return []
        tokens.append(('attr', first_ident))
        while i < n:
            if key[i] == '.':
                i += 1
                start = i
                while i < n and key[i] not in ('.', '['):
                    i += 1
                sub = key[start:i].strip()
                if sub:
                    tokens.append(('attr', sub))
            elif key[i] == '[':
                i += 1
                start = i
                while i < n and key[i] != ']':
                    i += 1
                bracket_content = key[start:i].strip()
                if i < n and key[i] == ']':
                    i += 1
                if (bracket_content.startswith("'") and bracket_content.endswith("'")) or \
                   (bracket_content.startswith('"') and bracket_content.endswith('"')):
                    tokens.append(('item', bracket_content[1:-1]))
                elif bracket_content.isdigit():
                    tokens.append(('item', int(bracket_content)))
                else:
                    tokens.append(('item', bracket_content))
            else:
                i += 1
        return tokens

    def _cheat_get_nested_val(key, default=None):
        try:
            tokens = _cheat_tokenize_path(key)
            if not tokens:
                return default
            target = renpy.store
            for t_type, t_val in tokens:
                if t_type == 'attr':
                    if not hasattr(target, t_val):
                        return default
                    target = getattr(target, t_val)
                elif t_type == 'item':
                    if isinstance(target, dict) or hasattr(target, '__getitem__'):
                        try:
                            target = target[t_val]
                        except (KeyError, IndexError, TypeError):
                            return default
                    else:
                        return default
            return target
        except Exception:
            return default

    def _cheat_clamp_val_to_game_max(target, attr_name, val, key=""):
        """
        Tự động kiểm tra và giới hạn giá trị cheat về mức tối đa mà game có thể chạy được:
        - Giới hạn theo mảng dữ liệu phụ thuộc (ví dụ job.pay, Job_level, levels, stages, ranks...)
        - Giới hạn theo thuộc tính Max tương ứng của đối tượng (max_hp, maxstamina, max_exp...)
        - Giới hạn các hằng số Max toàn cục trong store (MAX_LEVEL, MAX_STAMINA, CAP_...)
        - Giới hạn các chỉ số chu kỳ thời gian (hour <= 23, minute <= 59...)
        - Giới hạn các chỉ số phần trăm / tỷ lệ (0 - 100 hoặc 0.0 - 1.0)
        - Giới hạn an toàn chống tràn số nguyên 32-bit (2147483647)
        - Chặn số âm cho các chỉ số không thể âm
        """
        try:
            if not isinstance(val, _NUM_TYPES):
                return val

            attr_str = str(attr_name).lower() if attr_name is not None else ""
            key_str = str(key).lower() if key else attr_str

            # 1. Chống tràn số nguyên hệ thống 32-bit (tránh OverflowError trong Cython/C)
            if isinstance(val, int) and not isinstance(val, bool):
                if val > 2147483647:
                    val = 2147483647
                elif val < -2147483648:
                    val = -2147483648

            # 2. Chặn số âm cho các thuộc tính chỉ số game không âm
            non_neg_tags = ('skill', 'level', 'lvl', 'rank', 'grade', 'tier', 'idx', 'index',
                            'stage', 'phase', 'stamina', 'hp', 'mp', 'cash', 'money', 'gold',
                            'exp', 'point', 'pts', 'coin', 'coins', 'gem', 'gems', 'hunger',
                            'thirst', 'energy', 'health', 'pleasure', 'orgasm', 'orgasms',
                            'romance', 'love', 'affection', 'favor', 'lust', 'item', 'count',
                            'amount', 'qty', 'quantity', 'duration', 'shift', 'shifts')
            if any(tag in attr_str or tag in key_str for tag in non_neg_tags):
                if val < 0:
                    val = 0

            # 3. Kẹp theo danh sách / mảng phụ thuộc của đối tượng
            # 3.1. Skill / Level đối tượng có bảng lương pay (như Job, Place)
            if hasattr(target, 'pay'):
                p_list = getattr(target, 'pay', None)
                if isinstance(p_list, (list, tuple)) and len(p_list) > 0:
                    safe_limit = len(p_list) - 1
                    jl = getattr(renpy.store, 'Job_level', None)
                    if isinstance(jl, (list, tuple)) and len(jl) > 0:
                        safe_limit = min(safe_limit, len(jl) - 1)
                    if any(t in attr_str for t in ('skill', 'level', 'lvl', 'rank')):
                        if val > safe_limit:
                            val = safe_limit

            # 3.2. Level đối tượng có mảng levels / stages / ranks / tiers / phases / steps / slots
            for list_attr in ('levels', 'stages', 'ranks', 'tiers', 'phases', 'steps', 'slots'):
                if hasattr(target, list_attr):
                    dep_list = getattr(target, list_attr, None)
                    if isinstance(dep_list, (list, tuple)) and len(dep_list) > 0:
                        if any(t in attr_str for t in ('skill', 'level', 'lvl', 'rank', 'stage', 'phase', 'tier', 'step', 'slot')):
                            if val >= len(dep_list):
                                val = len(dep_list) - 1

            # 3.3. Đối tượng có bảng Job_level toàn cục trong store
            if any(t in attr_str for t in ('skill',)) or key_str.endswith('.skill'):
                jl = getattr(renpy.store, 'Job_level', None)
                if isinstance(jl, (list, tuple)) and len(jl) > 0:
                    if val >= len(jl):
                        val = len(jl) - 1

            # 4. Kẹp theo thuộc tính Max tương ứng trên đối tượng (max_... / max...)
            # Ví dụ: target.stamina kẹp theo target.maxstamina hoặc target.max_stamina
            if not attr_str.startswith('max') and not attr_str.endswith('_max') and not attr_str.endswith('max'):
                max_candidates = [
                    'max_' + attr_str,
                    'max' + attr_str,
                    attr_str + '_max',
                    attr_str + 'max'
                ]
                found_max = False
                for m_name in max_candidates:
                    if hasattr(target, m_name):
                        m_val = getattr(target, m_name, None)
                        if isinstance(m_val, _NUM_TYPES) and m_val > 0:
                            if val > m_val:
                                val = m_val
                            found_max = True
                            break
                # Nếu không có trên đối tượng, kiểm tra hằng số MAX toàn cục trong store
                if not found_max:
                    global_max_candidates = [
                        'MAX_' + attr_str.upper(),
                        'MAX' + attr_str.upper(),
                        attr_str.upper() + '_MAX',
                        attr_str.upper() + '_CAP',
                        attr_str.upper() + '_LIMIT'
                    ]
                    for gm_name in global_max_candidates:
                        if hasattr(renpy.store, gm_name):
                            gm_val = getattr(renpy.store, gm_name, None)
                            if isinstance(gm_val, _NUM_TYPES) and gm_val > 0:
                                if val > gm_val:
                                    val = gm_val
                                break

            # 5. Kẹp theo mảng danh sách toàn cục theo tên biến (ví dụ item_id kẹp theo items, chapter_idx kẹp theo chapters)
            for suffix in ('_id', '_idx', '_index', '_no', '_num'):
                if attr_str.endswith(suffix):
                    base_name = attr_str[:-len(suffix)]
                    for list_cand in (base_name + 's', base_name + '_list', base_name):
                        lst = getattr(target, list_cand, None) or getattr(renpy.store, list_cand, None)
                        if isinstance(lst, (list, tuple)) and len(lst) > 0:
                            if val >= len(lst):
                                val = len(lst) - 1
                            break

            # 6. Kẹp kinh nghiệm exp theo mức exp tối đa của cấp độ hiện tại (Job_level)
            if 'exp' in attr_str:
                curr_skill = getattr(target, 'skill', None)
                jl = getattr(renpy.store, 'Job_level', None)
                if isinstance(jl, (list, tuple)) and isinstance(curr_skill, _NUM_TYPES):
                    safe_s = max(0, min(int(curr_skill), len(jl) - 1))
                    if isinstance(jl[safe_s], (list, tuple)) and len(jl[safe_s]) > 1:
                        max_exp = jl[safe_s][1]
                        if isinstance(max_exp, _NUM_TYPES) and max_exp > 0:
                            if val > max_exp:
                                val = max_exp

            # 7. Kẹp các biến tỷ lệ / phần trăm
            pct_tags = ('percent', 'percentage', 'prob', 'probability', 'rate', 'chance', 'ratio')
            if any(tag in attr_str for tag in pct_tags):
                if isinstance(val, float):
                    cur_live = getattr(target, attr_name, None)
                    if cur_live is not None and 0.0 <= cur_live <= 1.0:
                        if val > 1.0:
                            val = 1.0
                    elif val > 100.0:
                        val = 100.0
                elif isinstance(val, _INT_TYPES):
                    if val > 100:
                        val = 100

            # 8. Kẹp các chỉ số thời gian / chu kỳ đồng hồ
            if attr_str in ('hour', 'hours'):
                if val > 23:
                    val = 23
            elif attr_str in ('minute', 'minutes', 'second', 'seconds'):
                if val > 59:
                    val = 59
            elif attr_str in ('day_of_week', 'weekday'):
                if val > 6:
                    val = 6
            elif attr_str in ('month', 'months'):
                if val > 12:
                    val = 12

            return val
        except Exception:
            return val

    def _cheat_set_nested_val(key, new_val, notify=True):
        try:
            tokens = _cheat_tokenize_path(key)
            if not tokens:
                return False
            target = renpy.store
            for t_type, t_val in tokens[:-1]:
                if t_type == 'attr':
                    if not hasattr(target, t_val):
                        return False
                    target = getattr(target, t_val)
                elif t_type == 'item':
                    if isinstance(target, dict) or hasattr(target, '__getitem__'):
                        try:
                            target = target[t_val]
                        except (KeyError, IndexError, TypeError):
                            return False
                    else:
                        return False
            last_type, last_val = tokens[-1]
            orig_input = new_val
            new_val = _cheat_clamp_val_to_game_max(target, last_val, new_val, key)
            if orig_input != new_val and notify:
                try:
                    cheat_notify("notify_max_clamp", str(new_val))
                except Exception:
                    pass
            if last_type == 'attr':
                setattr(target, last_val, new_val)
                return True
            elif last_type == 'item':
                if isinstance(target, (dict, list)) or hasattr(target, '__setitem__'):
                    try:
                        target[last_val] = new_val
                        return True
                    except (KeyError, IndexError, TypeError):
                        return False
            return False
        except Exception:
            return False

    def cheat_get_frozen_vars():
        f_dict = getattr(renpy.store, '_cheat_frozen_vars', None)
        if f_dict is None or not isinstance(f_dict, dict):
            p_frozen = getattr(persistent, 'cm_frozen_vars', None)
            renpy.store._cheat_frozen_vars = dict(p_frozen) if isinstance(p_frozen, dict) else {}
            f_dict = renpy.store._cheat_frozen_vars
        return f_dict

    class CheatMenuState(object):
        def __init__(self):
            self.current_tab = "vars"
            self.var_filter_type = "all"
            self.search_var_keyword = ""
            self.search_label_keyword = ""
            self.selected_amount = 100
            self.active_edit_var = None
            self.active_edit_type = None
            self.input_val = ""
            self.current_page = 0
            self.items_per_page = 10
            self.label_page = 0
            self.labels_per_page = 10
            self._cached_vars = None
            self._cached_filter_key = None

            # Quản lý sửa dịch văn bản (AI_trans_pry)
            self.search_trans_keyword = ""
            self.active_edit_trans_orig = None
            self.trans_edit_val = ""
            self.trans_view_mode = "history"
            self.research_game_input = ""
            self.txt_target_lang = "VI"
            self.txt_selected_file = None
            self.show_trans_dropdown = False
            self.show_lang_dropdown = False
            self.active_edit_char = None
            self.char_edit_preset = ""
            self.char_edit_self = ""
            self.char_edit_target = ""
            self.char_edit_tone = ""
            self.char_focus_field = "preset"

        def get_paged_vars(self):
            kw = self.search_var_keyword.lower().strip()
            filter_key = (self.var_filter_type, kw)
            if getattr(self, '_last_paging_filter_key', None) != filter_key:
                self._last_paging_filter_key = filter_key
                self.current_page = 0
            all_vars = self.get_all_game_vars()
            total = len(all_vars)
            max_pages = max(1, (total + self.items_per_page - 1) // self.items_per_page)
            if self.current_page >= max_pages:
                self.current_page = max_pages - 1
            if self.current_page < 0:
                self.current_page = 0
            start = self.current_page * self.items_per_page
            end = start + self.items_per_page
            slice_vars = all_vars[start:end]

            # Đọc giá trị trực tiếp (LIVE) theo thời gian thực từ renpy.store của file save đang chơi
            live_paged = []
            for item in slice_vars:
                v_name = item[0]
                cur_val = _cheat_get_nested_val(v_name, _CHEAT_NOT_FOUND)
                val = cur_val if cur_val is not _CHEAT_NOT_FOUND else item[1]
                v_type = item[2]
                if isinstance(val, bool):
                    v_type = "bool"
                elif isinstance(val, _NUM_TYPES):
                    v_type = "num"
                elif isinstance(val, _STR_TYPES):
                    v_type = "str"
                is_frozen = v_name in cheat_get_frozen_vars()
                is_pinned = v_name in persistent.cm_pinned_vars
                live_paged.append((v_name, val, v_type, is_frozen, is_pinned))
            return live_paged, total, self.current_page + 1, max_pages

        def prev_page(self):
            if self.current_page > 0:
                self.current_page -= 1
                renpy.restart_interaction()

        def next_page(self):
            all_vars = self.get_all_game_vars()
            max_pages = max(1, (len(all_vars) + self.items_per_page - 1) // self.items_per_page)
            if self.current_page < max_pages - 1:
                self.current_page += 1
                renpy.restart_interaction()

        def get_paged_labels(self):
            kw = self.search_label_keyword.lower().strip()
            if getattr(self, '_last_label_paging_kw', None) != kw:
                self._last_label_paging_kw = kw
                self.label_page = 0
            lbls = self.get_filtered_labels()
            total = len(lbls)
            max_pages = max(1, (total + self.labels_per_page - 1) // self.labels_per_page)
            if self.label_page >= max_pages:
                self.label_page = max_pages - 1
            if self.label_page < 0:
                self.label_page = 0
            start = self.label_page * self.labels_per_page
            end = start + self.labels_per_page
            return lbls[start:end], total, self.label_page + 1, max_pages

        def prev_label_page(self):
            if self.label_page > 0:
                self.label_page -= 1
                renpy.restart_interaction()

        def next_label_page(self):
            lbls = self.get_filtered_labels()
            max_pages = max(1, (len(lbls) + self.labels_per_page - 1) // self.labels_per_page)
            if self.label_page < max_pages - 1:
                self.label_page += 1
                renpy.restart_interaction()

        def invalidate_cache(self, reset_page=False):
            self._cached_vars = None
            self._cached_filter_key = None
            if reset_page:
                self.current_page = 0
                self.label_page = 0

        def step_val(self, key, delta):
            """Tăng/giảm giá trị số dựa trên giá trị thời gian thực của file save."""
            curr = _cheat_get_nested_val(key, _CHEAT_NOT_FOUND)
            if curr is _CHEAT_NOT_FOUND or curr is None:
                curr = 0
            try:
                if isinstance(curr, float):
                    new_val = round(curr + delta, 4)
                else:
                    new_val = int(curr) + delta
            except Exception:
                try:
                    new_val = float(curr) + delta
                except Exception:
                    new_val = delta
            self.set_val(key, new_val)

        def toggle_bool(self, key):
            """Đảo trạng thái Boolean dựa trên giá trị thời gian thực của file save."""
            curr = _cheat_get_nested_val(key, False)
            new_val = not bool(curr)
            self.set_val(key, new_val)

        def open_var_editor(self, var_name, current_val, v_type="num"):
            self.active_edit_var = var_name
            self.active_edit_type = v_type
            live = _cheat_get_nested_val(var_name, _CHEAT_NOT_FOUND)
            if live is not _CHEAT_NOT_FOUND:
                current_val = live
            self.input_val = _safe_str(current_val)
            renpy.restart_interaction()

        def open_number_editor(self, var_name, current_val):
            self.open_var_editor(var_name, current_val, "num")

        def open_str_editor(self, var_name, current_val):
            self.open_var_editor(var_name, current_val, "str")

        def apply_input_val(self):
            if not self.active_edit_var:
                return
            raw = self.input_val
            edit_type = getattr(self, 'active_edit_type', None)
            if edit_type == 'str':
                new_val = raw
            else:
                raw_s = raw.strip()
                if not raw_s:
                    raw_s = "0"
                try:
                    if '.' in raw_s:
                        new_val = float(raw_s)
                    else:
                        new_val = int(raw_s)
                except Exception:
                    try:
                        new_val = int(float(raw_s))
                    except Exception:
                        cheat_notify("notify_invalid_number")
                        return

                # Bảo toàn kiểu float nếu biến gốc là float
                cur_live = _cheat_get_nested_val(self.active_edit_var, _CHEAT_NOT_FOUND)
                if cur_live is not _CHEAT_NOT_FOUND and isinstance(cur_live, float) and not isinstance(new_val, float):
                    new_val = float(new_val)

            self.set_val(self.active_edit_var, new_val)
            self.active_edit_var = None
            self.active_edit_type = None
            renpy.restart_interaction()

        def cancel_editor(self):
            self.active_edit_var = None
            self.active_edit_type = None
            renpy.restart_interaction()

        # --- HỖ TRỢ DỊCH THUẬT & PERSONA (ỦY THÁC SANG CHEAT_TRANSLATE) ---
        def open_trans_editor(self, orig_text, current_trans):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.open_trans_editor(orig_text, current_trans)
            self.active_edit_trans_orig = orig_text
            self.trans_edit_val = _safe_str(current_trans)
            renpy.restart_interaction()

        def apply_trans_edit(self):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.apply_trans_edit()
            self.active_edit_trans_orig = None
            self.trans_edit_val = ""
            renpy.restart_interaction()

        def cancel_trans_editor(self):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.cancel_trans_editor()
            self.active_edit_trans_orig = None
            self.trans_edit_val = ""
            renpy.restart_interaction()

        def get_trans_list(self):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.get_trans_list()
            return []

        def get_character_list(self):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.get_character_list()
            return []

        def cycle_char_relation(self, who_name):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.cycle_char_relation(who_name)

        def open_char_editor(self, who_name, preset="", self_p="", target_p="", tone="", focus_field="preset"):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.open_char_editor(who_name, preset, self_p, target_p, tone, focus_field)

        def quick_set_char_pronouns(self, preset_name, self_p, target_p, tone="sweet"):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.quick_set_char_pronouns(preset_name, self_p, target_p, tone)

        def apply_char_edit(self):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.apply_char_edit()

        def cancel_char_editor(self):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.cancel_char_editor()

        def toggle_ai_offline(self):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.toggle_ai_offline()

        def force_ai_save(self):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.force_ai_save()

        def trigger_story_research(self, custom_title=None):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.trigger_story_research(custom_title)

        def get_research_status(self):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.get_research_status()
            return {"status": "idle", "message": "", "progress": 0}

        def get_story_context(self):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.get_story_context()
            return {}

        def export_b1_txt(self):
            cheat_notify("notify_export_merged")
            renpy.restart_interaction()

        def toggle_auto_translate(self):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.toggle_auto_translate()
            curr = getattr(persistent, 'cm_auto_translate', False)
            persistent.cm_auto_translate = not curr
            renpy.restart_interaction()

        def switch_trans_lang(self, lang_code):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.switch_trans_lang(lang_code)

        def start_b2_translation(self):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.start_b2_translation()

        def stop_b2_translation(self):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.stop_b2_translation()

        def apply_b3_txt(self):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.apply_b3_txt()

        def get_b2_progress(self):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.get_b2_progress()
            return {"status": "idle", "current": 0, "total": 0, "percent": 0, "message": ""}

        def get_available_trans_files(self):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.get_available_trans_files()
            return {"ol_files": [], "trans_files": []}

        def open_translate_folder(self):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.open_translate_folder()

        def open_trans_font_folder(self):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.open_trans_font_folder()

        def get_trans_font_name(self):
            ct = getattr(renpy.store, 'cheat_trans_state', None)
            if ct:
                return ct.get_trans_font_name()
            return "Mặc định"


        def get_all_game_vars(self):
            kw = self.search_var_keyword.lower().strip()
            filter_key = (self.var_filter_type, kw)
            if self._cached_vars is not None and self._cached_filter_key == filter_key:
                return self._cached_vars

            result = []
            store_dict = renpy.store.__dict__
            synonyms = STAT_KEYWORD_SYNONYMS.get(kw, ())

            def check_and_add(var_name, val, v_type):
                if self.var_filter_type != "all" and self.var_filter_type != v_type:
                    return

                if kw:
                    var_name_lower = var_name.lower()
                    match_name = (kw in var_name_lower)
                    val_str = _safe_str(val).lower()
                    match_val = (kw == val_str or (len(kw) >= 2 and kw in val_str))
                    match_syn = any(syn in var_name_lower for syn in synonyms)
                    if not (match_name or match_val or match_syn):
                        return

                is_frozen = var_name in cheat_get_frozen_vars()
                is_pinned = var_name in persistent.cm_pinned_vars
                is_common_stat = _cheat_is_common_stat(var_name)
                result.append((var_name, val, v_type, is_frozen, is_pinned, is_common_stat))

            for key, val in list(store_dict.items()):
                if key.startswith('_') or key in IGNORED_STORE_KEYS:
                    continue
                if callable(val) or type(val).__name__ in ('module', 'type', 'classobj'):
                    continue

                if isinstance(val, bool):
                    check_and_add(key, val, "bool")
                elif isinstance(val, _NUM_TYPES):
                    check_and_add(key, val, "num")
                elif isinstance(val, _STR_TYPES):
                    check_and_add(key, val, "str")
                else:
                    # Tìm kiếm các chỉ số lồng trong đối tượng game (VD: player.money, mc.hp, hero.str)
                    if hasattr(val, '__dict__'):
                        try:
                            for sub_k, sub_v in list(val.__dict__.items()):
                                if sub_k.startswith('_') or callable(sub_v):
                                    continue
                                full_key = "%s.%s" % (key, sub_k)
                                if isinstance(sub_v, bool):
                                    check_and_add(full_key, sub_v, "bool")
                                elif isinstance(sub_v, _NUM_TYPES):
                                    check_and_add(full_key, sub_v, "num")
                                elif isinstance(sub_v, _STR_TYPES) and len(sub_v) < 60:
                                    check_and_add(full_key, sub_v, "str")
                        except Exception:
                            pass
                    elif isinstance(val, dict) and len(val) < 200:
                        try:
                            for sub_k, sub_v in list(val.items()):
                                if not isinstance(sub_k, _STR_TYPES) or sub_k.startswith('_') or callable(sub_v):
                                    continue
                                full_key = "%s['%s']" % (key, sub_k)
                                if isinstance(sub_v, bool):
                                    check_and_add(full_key, sub_v, "bool")
                                elif isinstance(sub_v, _NUM_TYPES):
                                    check_and_add(full_key, sub_v, "num")
                                elif isinstance(sub_v, _STR_TYPES) and len(sub_v) < 60:
                                    check_and_add(full_key, sub_v, "str")
                        except Exception:
                            pass

            # Sắp xếp: 1. Ghim lên đầu -> 2. Chỉ số game quan trọng -> 3. Tên chữ cái
            result.sort(key=lambda item: (not item[4], not item[5], item[0].lower()))
            clean_result = [(it[0], it[1], it[2], it[3], it[4]) for it in result]
            self._cached_vars = clean_result
            self._cached_filter_key = filter_key
            return clean_result

        def get_filtered_labels(self):
            kw = self.search_label_keyword.lower().strip()
            labels = []
            try:
                all_lbls = renpy.get_all_labels()
                for lbl in all_lbls:
                    if lbl.startswith('_') or lbl.startswith('gui_') or 'hide' in lbl:
                        continue
                    if kw and kw not in lbl.lower():
                        continue
                    labels.append(lbl)
            except Exception:
                pass
            labels.sort()
            return labels

        def set_val(self, key, new_val):
            try:
                _cheat_set_nested_val(key, new_val, notify=True)
                actual_val = _cheat_get_nested_val(key, new_val)
                f_dict = cheat_get_frozen_vars()
                if key in f_dict:
                    f_dict[key] = actual_val
                    persistent.cm_frozen_vars[key] = actual_val
                # get_paged_vars đọc live thời gian thực nên không cần quét lại biến toàn game, thao tác mượt mà 100%
                renpy.restart_interaction()
            except Exception:
                pass

        def toggle_freeze(self, key):
            f_dict = cheat_get_frozen_vars()
            if key in f_dict:
                del f_dict[key]
                if key in persistent.cm_frozen_vars:
                    del persistent.cm_frozen_vars[key]
            else:
                live_v = _cheat_get_nested_val(key)
                f_dict[key] = live_v
                persistent.cm_frozen_vars[key] = live_v
            renpy.restart_interaction()

        def toggle_pin(self, key):
            if key in persistent.cm_pinned_vars:
                persistent.cm_pinned_vars.remove(key)
            else:
                persistent.cm_pinned_vars.append(key)
            self.invalidate_cache(reset_page=False)
            renpy.restart_interaction()

    cheat_menu_state = CheatMenuState()

    def cheat_menu_freezer_callback():
        f_dict = cheat_get_frozen_vars()
        if not f_dict:
            return
        for k, v in list(f_dict.items()):
            try:
                curr = _cheat_get_nested_val(k, _CHEAT_NOT_FOUND)
                if curr is not _CHEAT_NOT_FOUND and curr != v:
                    _cheat_set_nested_val(k, v, notify=False)
            except Exception:
                pass

    _interact_cbs = _safe_get_config('interact_callbacks', None)
    if _interact_cbs is not None and isinstance(_interact_cbs, list) and cheat_menu_freezer_callback not in _interact_cbs:
        _interact_cbs.append(cheat_menu_freezer_callback)

    # --------------------------------------------------------------------------
    # 6. ĐIỀU KHIỂN TỐC ĐỘ GAME (ĐÃ VÔ HIỆU HÓA THEO YÊU CẦU)
    # --------------------------------------------------------------------------
    def cheat_apply_speed(multiplier=1.0):
        pass

    def cheat_step_speed(delta=0.0):
        pass

    def cheat_nudge_bar_y(delta):
        curr = getattr(persistent, 'cm_bar_y', 140) or 140
        try:
            curr = int(curr)
        except Exception:
            curr = 140
        persistent.cm_bar_y = max(10, min(600, curr + delta))
        renpy.restart_interaction()

    def cheat_unlock_all_gallery():
        try:
            # 1. Mở khóa toàn bộ ảnh bằng API chuẩn của Ren'Py
            if hasattr(renpy, 'list_images'):
                all_imgs = renpy.list_images()
            elif hasattr(renpy.exports, 'list_images'):
                all_imgs = renpy.exports.list_images()
            else:
                all_imgs = []

            for img in all_imgs:
                try:
                    if hasattr(renpy, 'seen_image'):
                        renpy.seen_image(img)
                    elif hasattr(renpy.exports, 'seen_image'):
                        renpy.exports.seen_image(img)
                except Exception:
                    pass

            # 2. Mở khóa toàn bộ nhạc/âm thanh trong game (Music Gallery)
            try:
                files_list = renpy.list_files() if hasattr(renpy, 'list_files') else (renpy.exports.list_files() if hasattr(renpy.exports, 'list_files') else [])
                for f_name in files_list:
                    f_lower = f_name.lower()
                    if any(f_lower.endswith(ext) for ext in ('.mp3', '.ogg', '.opus', '.wav', '.flac')):
                        try:
                            if hasattr(renpy, 'seen_audio'):
                                renpy.seen_audio(f_name)
                            elif hasattr(renpy.exports, 'seen_audio'):
                                renpy.exports.seen_audio(f_name)
                        except Exception:
                            pass
            except Exception:
                pass

            # 3. Mở khóa cờ Gallery/CG/Replay do tác giả game đặt (hỗ trợ cả dict và cấp ngoài)
            for k in list(persistent.__dict__.keys()):
                if k.startswith('_'):
                    continue
                k_lower = k.lower()
                is_gallery_target = any(tag in k_lower for tag in ('unlock', 'gallery', 'cg', 'replay', 'bonus', 'scene', 'scenes', 'art', 'memory', 'photo'))
                val = getattr(persistent, k, None)
                if is_gallery_target:
                    if isinstance(val, (bool, type(None))):
                        setattr(persistent, k, True)
                    elif isinstance(val, _NUM_TYPES) and not isinstance(val, bool):
                        setattr(persistent, k, max(val, 1))
                    elif isinstance(val, dict):
                        for sub_k in list(val.keys()):
                            if isinstance(val[sub_k], bool):
                                val[sub_k] = True
                            elif isinstance(val[sub_k], _NUM_TYPES) and not isinstance(val[sub_k], bool):
                                val[sub_k] = max(val[sub_k], 1)
                elif isinstance(val, dict) and any(tag in k_lower for tag in ('gallery', 'cg', 'replay', 'scenes')):
                    for sub_k in list(val.keys()):
                        if isinstance(val[sub_k], bool):
                            val[sub_k] = True
                        elif isinstance(val[sub_k], _NUM_TYPES) and not isinstance(val[sub_k], bool):
                            val[sub_k] = max(val[sub_k], 1)

            # 4. Mở khóa các từ điển Gallery lưu trong renpy.store
            for s_key in ('g_unlocked', 'gallery_unlocked', 'cg_unlocked', 'unlocked_cg', 'scenes_unlocked', 'gallery_items'):
                s_val = getattr(renpy.store, s_key, None)
                if isinstance(s_val, dict):
                    for sub_k in list(s_val.keys()):
                        if isinstance(s_val[sub_k], bool):
                            s_val[sub_k] = True
                        elif isinstance(s_val[sub_k], _NUM_TYPES) and not isinstance(s_val[sub_k], bool):
                            s_val[sub_k] = max(s_val[sub_k], 1)

            renpy.save_persistent()
            cheat_notify("notify_gallery_unlocked")
        except Exception as e:
            cheat_notify("notify_error_prefix", str(e))

    # Developer console (An toàn đa phiên bản)
    _safe_set_config('developer', True)
    _safe_set_config('console', True)

    def cheat_enable_developer():
        _safe_set_config('developer', True)
        _safe_set_config('console', True)
        renpy.restart_interaction()

    def cheat_enable_force_skip_permanent():
        _safe_set_config('fast_skipping', True)
        _safe_set_config('allow_skipping', True)
        _safe_set_pref('skip_unseen', True)
        cheat_notify("notify_force_skip_on")
        renpy.restart_interaction()

    def cheat_can_jump_safely():
        """Kiểm tra xem có an toàn để Jump/Call không (tránh crash khi đang ở Main Menu)."""
        try:
            if renpy.get_screen('main_menu'):
                return False
            ctx = renpy.context()
            if getattr(ctx, 'main_menu', False):
                return False
        except Exception:
            pass
        return True

    def cheat_safe_jump(lbl):
        if not cheat_can_jump_safely():
            cheat_notify("notify_need_game_jump")
            return
        renpy.hide_screen('cheat_main_modal')
        try:
            if hasattr(renpy.exports, 'Jump'):
                renpy.run(renpy.exports.Jump(lbl))
            else:
                renpy.jump(lbl)
        except Exception:
            try:
                renpy.jump(lbl)
            except Exception as e:
                cheat_notify("notify_jump_failed", str(e))

    def cheat_safe_call(lbl):
        if not cheat_can_jump_safely():
            cheat_notify("notify_need_game_call")
            return
        renpy.hide_screen('cheat_main_modal')
        try:
            if hasattr(renpy.exports, 'Call'):
                renpy.run(renpy.exports.Call(lbl))
            else:
                renpy.call_in_new_context(lbl)
        except Exception:
            try:
                renpy.call(lbl)
            except Exception as e:
                cheat_notify("notify_call_failed", str(e))

    def cheat_toggle_auto_forward():
        """Bật/tắt Auto-Forward, tự động khởi tạo thời gian afm nếu đang bằng 0."""
        try:
            curr_afm = getattr(_preferences, 'afm_time', 0)
            if curr_afm is None or curr_afm <= 0:
                _preferences.afm_time = 15.0
            _preferences.afm_enable = not getattr(_preferences, 'afm_enable', True)
        except Exception:
            pass
        try:
            renpy.run(Preference("auto-forward", "toggle"))
        except Exception:
            pass
        renpy.restart_interaction()

    def cheat_is_text_input_active():
        """Kiểm tra động xem người chơi có đang trong bất kỳ ô nhập văn bản (Input) nào không."""
        try:
            # 1. Kiểm tra widget đang được focus
            if hasattr(renpy, 'display') and hasattr(renpy.display, 'focus'):
                focused = getattr(renpy.display.focus, 'focused', None)
                if focused is not None:
                    cls_name = getattr(focused, '__class__', None)
                    if cls_name and getattr(cls_name, '__name__', '') == 'Input':
                        return True
            # 2. Kiểm tra nếu Cheat Menu đang mở chế độ sửa biến hoặc sửa dịch
            if getattr(renpy.store, 'cheat_menu_state', None):
                cms = renpy.store.cheat_menu_state
                if getattr(cms, 'active_edit_var', None) is not None or getattr(cms, 'active_edit_trans_orig', None) is not None:
                    return True
            # 3. Quét các màn hình input đặt tên nhân vật thường gặp
            input_screens = ('input', 'name_input', 'enter_name', 'char_custom', 'naming', 'phone_input', 'type_name', 'naming_screen', 'character_creation')
            for s in input_screens:
                if renpy.get_screen(s):
                    return True
            if renpy.get_screen('_console') or renpy.get_screen('console'):
                return True
        except Exception:
            pass
        return False

    def cheat_is_wheel_scroll_allowed():
        """
        Kiểm tra xem con lăn chuột có đang cần dùng để cuộn nội dung hay không:
        - Màn hình lựa chọn (Choice screen): khi danh sách lựa chọn dài cần lăn chuột để xem hết.
        - Các màn hình hệ thống có thanh cuộn (Save, Load, History, Preferences, Help, About...).
        - Khi các màn hình này hiển thị, KHÔNG can thiệp để người chơi tự do lăn chuột 100%!
        """
        try:
            scroll_screens = (
                'choice', 'nvl_choice', 'menu', 'choice_screen', 'nvl_menu',
                'save', 'load', 'file_slots', 'file_picker',
                'history', 'text_history', 'cheat_history_modal',
                'preferences', 'help', 'about'
            )
            for s in scroll_screens:
                if renpy.get_screen(s):
                    return True
        except Exception:
            pass
        return False

    _last_auto_repair_ts = 0.0

    def _cheat_auto_repair_game_data(force=False):
        """
        Tự động cứu hộ và sửa lỗi nếu người chơi vô tình cheat chỉ số quá cao
        dẫn đến tràn index danh sách trong code game (Ví dụ: j.pay[j.skill] bị IndexError).
        """
        global _last_auto_repair_ts
        now = time.time()
        if not force and (now - _last_auto_repair_ts < 2.0):
            return
        _last_auto_repair_ts = now
        try:
            jl = getattr(renpy.store, 'Job_level', None)
            jl_len = len(jl) if isinstance(jl, (list, tuple)) else None

            def _fix_game_obj(obj, depth=0):
                if not obj or depth > 3:
                    return

                # 1. Sửa obj nếu có skill và pay / Job_level
                if hasattr(obj, 'skill'):
                    s_val = getattr(obj, 'skill', None)
                    if isinstance(s_val, _NUM_TYPES):
                        limit = None
                        if hasattr(obj, 'pay'):
                            p_list = getattr(obj, 'pay', None)
                            if isinstance(p_list, (list, tuple)) and len(p_list) > 0:
                                limit = len(p_list) - 1
                        if jl_len is not None and jl_len > 0:
                            limit = min(limit, jl_len - 1) if limit is not None else (jl_len - 1)
                        if limit is not None and s_val > limit:
                            setattr(obj, 'skill', limit)
                        elif s_val < 0:
                            setattr(obj, 'skill', 0)

                # 2. Sửa obj nếu có stamina và maxstamina
                if hasattr(obj, 'stamina'):
                    cur_st = getattr(obj, 'stamina', None)
                    max_st = getattr(obj, 'maxstamina', None) or getattr(obj, 'max_stamina', None)
                    if isinstance(cur_st, _NUM_TYPES) and isinstance(max_st, _NUM_TYPES) and max_st > 0:
                        if cur_st > max_st:
                            setattr(obj, 'stamina', max_st)
                        elif cur_st < 0:
                            setattr(obj, 'stamina', 0)

                # 3. Sửa obj nếu có hp và max_hp
                if hasattr(obj, 'hp'):
                    cur_hp = getattr(obj, 'hp', None)
                    max_hp = getattr(obj, 'max_hp', None) or getattr(obj, 'maxhp', None)
                    if isinstance(cur_hp, _NUM_TYPES) and isinstance(max_hp, _NUM_TYPES) and max_hp > 0:
                        if cur_hp > max_hp:
                            setattr(obj, 'hp', max_hp)
                        elif cur_hp < 0:
                            setattr(obj, 'hp', 0)

                # 4. Kiểm tra các thuộc tính con và cấu trúc lồng nhau
                for sub_attr in ('job', 'unit', 'locales', 'places', 'chars'):
                    if hasattr(obj, sub_attr):
                        val = getattr(obj, sub_attr, None)
                        if isinstance(val, (list, tuple)):
                            for item in val:
                                _fix_game_obj(item, depth + 1)
                        else:
                            _fix_game_obj(val, depth + 1)

            for k, val in list(renpy.store.__dict__.items()):
                if k.startswith('_'):
                    continue
                _fix_game_obj(val)
                if isinstance(val, dict) and len(val) < 100:
                    for sub_v in list(val.values()):
                        _fix_game_obj(sub_v)
                elif isinstance(val, (list, tuple)) and len(val) < 100:
                    for sub_v in val:
                        _fix_game_obj(sub_v)
        except Exception:
            pass

    def cheat_set_max_val(v_name):
        """Đặt giá trị tối đa an toàn, tự động tính toán theo giới hạn dữ liệu tối đa mà game có thể chạy được."""
        try:
            tokens = _cheat_tokenize_path(v_name)
            target = renpy.store
            attr_name = v_name
            if tokens:
                for t_type, t_val in tokens[:-1]:
                    if t_type == 'attr' and hasattr(target, t_val):
                        target = getattr(target, t_val)
                    elif t_type == 'item' and hasattr(target, '__getitem__'):
                        try:
                            target = target[t_val]
                        except Exception:
                            pass
                attr_name = tokens[-1][1]

            desired_max = 999999999
            safe_max = _cheat_clamp_val_to_game_max(target, attr_name, desired_max, v_name)
            cheat_menu_state.set_val(v_name, safe_max)
            if safe_max != desired_max:
                cheat_notify("notify_clamped_game_max", str(safe_max))
            else:
                cheat_notify("notify_max_value_set", str(safe_max))
        except Exception:
            cheat_menu_state.set_val(v_name, 999999)

    # --------------------------------------------------------------------------
    # 7. BỘ CỨU HỘ SỰ CỐ & TỰ ĐỘNG KHẮC PHỤC KHI CHƠI GAME (CRASH IMMUNITY ENGINE)
    # --------------------------------------------------------------------------
    def _cheat_global_exception_handler(short, full, traceback_fn):
        """
        Tự động bắt lỗi trong lúc chơi game, tự sửa dữ liệu biến tràn/hỏng,
        và giải cứu game tiếp tục chạy thay vì văng crash sập ra ngoài desktop.
        """
        try:
            # 1. Tự động sửa chữa khẩn cấp dữ liệu biến
            _cheat_auto_repair_game_data(force=True)

            # 2. Ghi chi tiết lỗi vào cheat_crash_log.txt để kiểm tra lại
            g_dir = _safe_get_config('gamedir', '.') or '.'
            log_path = os.path.join(g_dir, "cheat_crash_log.txt")
            try:
                with open(log_path, "a") as f:
                    f.write("\n" + "=" * 60 + "\n")
                    f.write("THỜI GIAN: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                    f.write("LỖI ĐÃ TỰ ĐỘNG BẮT VÀ XỬ LÝ AN TOÀN:\n")
                    f.write(str(short) + "\n\n")
                    f.write(str(full) + "\n")
            except Exception:
                pass

            # 3. Hiện thông báo cho người chơi biết game vừa tự động giải cứu
            err_line = str(short).splitlines()[0] if str(short) else "Lỗi kịch bản game"
            cheat_notify("notify_crash_intercepted", err_line[:50])

            # 4. Cho phép game tiếp tục bỏ qua lệnh lỗi nếu tính năng tự cứu hộ đang bật
            if getattr(persistent, 'cm_auto_recover_crash', True):
                return True
        except Exception:
            pass
        return False

    # --------------------------------------------------------------------------
    # 8. TỰ ĐỘNG CẬP NHẬT & ĐỒNG BỘ MỌI GAME (AUTO-SYNC ENGINE)
    # --------------------------------------------------------------------------
    def _cheat_auto_sync_from_master():
        """
        Tự động kiểm tra và đồng bộ bản cheat_menu.rpy mới nhất từ thư mục Master:
        G:\TeraBoxDownload\Cheat menu Renply\cheat_menu.rpy
        """
        try:
            master_file = r"G:\TeraBoxDownload\Cheat menu Renply\cheat_menu.rpy"
            if not os.path.exists(master_file):
                return

            g_dir = _safe_get_config('gamedir', '.') or '.'
            curr_file = os.path.join(g_dir, "cheat_menu.rpy")
            if not os.path.exists(curr_file):
                return

            try:
                if os.path.samefile(master_file, curr_file):
                    return
            except Exception:
                if os.path.abspath(master_file).lower() == os.path.abspath(curr_file).lower():
                    return

            m_size = os.path.getsize(master_file)
            c_size = os.path.getsize(curr_file)
            m_mtime = os.path.getmtime(master_file)
            c_mtime = os.path.getmtime(curr_file)

            if m_mtime > c_mtime + 2 or m_size != c_size:
                import shutil
                shutil.copy2(master_file, curr_file)
                rpyc = curr_file + 'c'
                if os.path.exists(rpyc):
                    try:
                        os.remove(rpyc)
                    except Exception:
                        pass

                # Tự động nạp lại kịch bản (Hot-Reload) tức thì ngay trong lần mở game này
                if hasattr(renpy, 'session') and not renpy.session.get('_cheat_hot_reloaded', False):
                    renpy.session['_cheat_hot_reloaded'] = True
                    if hasattr(renpy, 'utter_restart'):
                        renpy.utter_restart()
        except Exception:
            pass

    def cheat_sync_all_games():
        """
        Nút bấm 1-Click: Tự động quét và đồng bộ cheat_menu.rpy cho TẤT CẢ các game
        trong G:\TeraBoxDownload\Ren'Py ngay từ trong giao diện.
        """
        try:
            g_dir = _safe_get_config('gamedir', '.') or '.'
            src_file = os.path.join(g_dir, "cheat_menu.rpy")
            master_file = r"G:\TeraBoxDownload\Cheat menu Renply\cheat_menu.rpy"

            if os.path.exists(master_file):
                src = master_file
            elif os.path.exists(src_file):
                src = src_file
            else:
                cheat_notify("notify_sync_src_not_found")
                return

            renpy_root = r"G:\TeraBoxDownload\Ren'Py"
            if not os.path.exists(renpy_root):
                cheat_notify("notify_sync_dir_not_found", renpy_root)
                return

            import shutil
            count = 0
            for root, dirs, files in os.walk(renpy_root):
                if 'cheat_menu.rpy' in files and os.path.basename(root) == 'game':
                    dst = os.path.join(root, 'cheat_menu.rpy')
                    try:
                        shutil.copy2(src, dst)
                        rpyc = dst + 'c'
                        if os.path.exists(rpyc):
                            os.remove(rpyc)
                        count += 1
                    except Exception:
                        pass

            cheat_notify("notify_sync_done", count)
            renpy.restart_interaction()
        except Exception as e:
            cheat_notify("notify_sync_error", str(e))

    # Kích hoạt tự động đồng bộ khi mở bất kỳ game nào
    _cheat_auto_sync_from_master()

    # Thông báo nếu game vừa hoàn tất tự động cập nhật khi mở máy
    try:
        if hasattr(renpy, 'session') and renpy.session.get('_cheat_hot_reloaded', False):
            renpy.session['_cheat_hot_reloaded'] = False
            cheat_notify("notify_master_updated")
    except Exception:
        pass

    # Kích hoạt bộ cứu hộ bắt lỗi toàn cục
    _safe_set_config('exception_handler', _cheat_global_exception_handler)

# ==============================================================================
# PHÍM TẮT TOÀN CỤC
# ==============================================================================
screen cheat_global_keyhandler():
    zorder 2000
    if not renpy.get_screen('cheat_main_modal'):
        # Các phím mở menu chính (Hỗ trợ cả bàn phím chuẩn, Numpad, và không bị Unikey/EVKey nuốt)
        key 'K_TAB' action ToggleScreen('cheat_main_modal')
        key 'K_F1' action ToggleScreen('cheat_main_modal')
        key 'K_F2' action ToggleScreen('cheat_main_modal')
        key '`' action ToggleScreen('cheat_main_modal')
        key '~' action ToggleScreen('cheat_main_modal')
        key 'K_BACKQUOTE' action ToggleScreen('cheat_main_modal')
        key 'shift_K_BACKQUOTE' action ToggleScreen('cheat_main_modal')
        key 'alt_K_c' action ToggleScreen('cheat_main_modal')
        key 'shift_K_c' action ToggleScreen('cheat_main_modal')
        key '*' action [ToggleField(persistent, 'cm_bar_collapsed'), Function(renpy.restart_interaction)]
        key 'K_KP_MULTIPLY' action [ToggleField(persistent, 'cm_bar_collapsed'), Function(renpy.restart_interaction)]
        key 'alt_K_KP_MULTIPLY' action [ToggleField(persistent, 'cm_bar_visible'), Function(renpy.restart_interaction)]

        # Tránh cướp phím chữ khi người chơi đang gõ tên/nhập liệu hoặc chơi game dùng phím WASD
        if not cheat_is_text_input_active() and getattr(persistent, 'cm_single_key_shortcuts', True):
            key 'h' action HideInterface()
            key 'H' action HideInterface()
            key 's' action Function(cheat_toggle_force_skip)
            key 'S' action Function(cheat_toggle_force_skip)
            key 'a' action Function(cheat_toggle_auto_forward)
            key 'A' action Function(cheat_toggle_auto_forward)
            key 'l' action ToggleScreen("cheat_history_modal")
            key 'L' action ToggleScreen("cheat_history_modal")

            # Bảo vệ chống lỗi khi lăn chuột tua ngược lại (Rollback Protection)
            # TỰ ĐỘNG NHƯỜNG CON LĂN CHUỘT: Nếu đang ở màn hình lựa chọn (Choice) hoặc màn hình có thanh cuộn
            # thì KHÔNG can thiệp, để người chơi tự do lăn chuột xem hết tất cả các lựa chọn dài!
            if not cheat_is_wheel_scroll_allowed():
                $ _wheel_mode = getattr(persistent, 'cm_wheel_fix_mode', 'off')
                if _wheel_mode == 'history':
                    key 'mousedown_4' action Function(cheat_safe_show_history)
                elif _wheel_mode == 'disable':
                    key 'mousedown_4' action Function(cheat_dummy_func)
                    key 'mousedown_5' action Function(cheat_dummy_func)
    else:
        key 'K_TAB' action ToggleScreen('cheat_main_modal')
        key 'K_F1' action ToggleScreen('cheat_main_modal')
        key 'K_F2' action ToggleScreen('cheat_main_modal')
        key '`' action ToggleScreen('cheat_main_modal')
        key '~' action ToggleScreen('cheat_main_modal')
        key 'K_BACKQUOTE' action ToggleScreen('cheat_main_modal')
        key 'shift_K_BACKQUOTE' action ToggleScreen('cheat_main_modal')
        key 'alt_K_c' action ToggleScreen('cheat_main_modal')
        key 'shift_K_c' action ToggleScreen('cheat_main_modal')
        if cheat_menu_state.active_edit_var is None:
            key 'K_ESCAPE' action ToggleScreen('cheat_main_modal')

init 999 python:
    # 1. Ren'Py 7.6+ & 8.x: dùng config.always_shown_screens để thanh công cụ luôn hiện diện
    _always_list = _safe_get_config('always_shown_screens', None)
    if _always_list is not None and isinstance(_always_list, list):
        for _s in ('cheat_global_keyhandler', 'cheat_floating_bar'):
            if _s not in _always_list:
                _always_list.append(_s)

    # 2. Ren'Py 6 & 7.x (Overlay screens): fallback dự phòng
    _overlay_list = _safe_get_config('overlay_screens', None)
    if _overlay_list is not None and isinstance(_overlay_list, list):
        for _s in ('cheat_global_keyhandler', 'cheat_floating_bar'):
            if _s not in _overlay_list:
                _overlay_list.append(_s)

    # 3. Đảm bảo screen luôn được nạp lại ở mọi tương tác của game (scene mới, chọn choice, đổi label...)
    def _cheat_ensure_active_screens():
        try:
            _cheat_auto_repair_game_data()
            if getattr(persistent, 'cm_wheel_fix_mode', 'off') != 'off' or getattr(persistent, 'cm_disable_rollback', False):
                cheat_apply_wheel_protection()
            if not renpy.get_screen('cheat_global_keyhandler'):
                renpy.show_screen('cheat_global_keyhandler')
            if getattr(persistent, 'cm_bar_visible', True):
                if not renpy.get_screen('cheat_floating_bar'):
                    renpy.show_screen('cheat_floating_bar')
            else:
                if renpy.get_screen('cheat_floating_bar'):
                    renpy.hide_screen('cheat_floating_bar')
        except Exception:
            pass

    # Gắn vào mọi vòng đời sự kiện của Ren'Py:
    for _cb_name in ('start_callbacks', 'after_load_callbacks', 'interact_callbacks', 'scene_callbacks'):
        _c_list = _safe_get_config(_cb_name, None)
        if _c_list is not None and isinstance(_c_list, list) and _cheat_ensure_active_screens not in _c_list:
            _c_list.append(_cheat_ensure_active_screens)

    # 4. Tự động đồng bộ và cập nhật chỉ số Cheat Menu ngay khi vào bất kỳ file save game nào
    def _cheat_on_save_load_or_start():
        try:
            _cheat_auto_repair_game_data(force=True)
            # Xóa cache danh sách biến để quét lại chuẩn xác 100% theo file save mới vừa nạp
            cheat_menu_state.invalidate_cache(reset_page=False)
            cheat_menu_state.active_edit_var = None
            cheat_menu_state.active_edit_type = None

            # Phục hồi danh sách biến bị khóa từ save game vừa nạp (không bị mất khóa khi load)
            f_dict = getattr(renpy.store, '_cheat_frozen_vars', None)
            if isinstance(f_dict, dict):
                persistent.cm_frozen_vars = dict(f_dict)
            else:
                if getattr(persistent, 'cm_frozen_vars', None):
                    persistent.cm_frozen_vars.clear()

            renpy.restart_interaction()
        except Exception:
            pass

    for _cb_name in ('start_callbacks', 'after_load_callbacks'):
        _c_list = _safe_get_config(_cb_name, None)
        if _c_list is not None and isinstance(_c_list, list) and _cheat_on_save_load_or_start not in _c_list:
            _c_list.append(_cheat_on_save_load_or_start)
        elif _c_list is None:
            _safe_set_config(_cb_name, [_cheat_on_save_load_or_start])

# ==============================================================================
# HỆ THỐNG PHÓNG THÍCH ĐỒNG NHẤT (UNIVERSAL AUTO-SCALING ENGINE)
# ==============================================================================
transform cheat_modal_scaler(z=1.0):
    subpixel True
    transform_anchor True
    align (0.5, 0.5)
    zoom z

transform cheat_bar_scaler(z=1.0, y_pos=140):
    subpixel True
    transform_anchor True
    xpos 1.0
    xanchor 1.0
    ypos y_pos
    yanchor 0.0
    zoom z

# ==============================================================================
# SCREEN 1: THANH CÔNG CỤ NỔI DỌC MÉP PHẢI (CHUẨN GIAO DIỆN HIDESKIPMENU)
# ==============================================================================
screen cheat_floating_bar():
    zorder 2000
    style_prefix "cheat"
    $ _t = cheat_tr

    if getattr(persistent, 'cm_bar_visible', True):
        $ _cm_scale = cheat_get_ui_scale()
        $ _bar_y = cheat_get_bar_y()
        frame:
            at cheat_bar_scaler(_cm_scale, _bar_y)
            background None
            padding (0, 0)
            margin (0, 0)

            hbox:
                spacing 0

                # 1. TAB ĐÓNG / MỞ MENU (NẰM Ở MẶT NGOÀI BÊN TRÁI PANEL, NỔI BẬT DỄ THẤY)
                button:
                    action [ToggleField(persistent, 'cm_bar_collapsed'), Function(renpy.restart_interaction)]
                    yalign 0.0
                    yoffset 10
                    xsize 34
                    ysize 66
                    background ("#0284c7ee" if getattr(persistent, 'cm_bar_collapsed', True) else "#0f172aee")
                    hover_background "#38bdf8"
                    vbox:
                        align (0.5, 0.5)
                        spacing 2
                        text "⚡" size 15 bold True color "#ffffff" align (0.5, 0.5)
                        text (">" if not getattr(persistent, 'cm_bar_collapsed', True) else "<"):
                            align (0.5, 0.5)
                            size 15
                            bold True
                            color "#ffffff"

                # 2. KHUNG NỘI DUNG SIDEBAR (RỘNG 205PX, THEME DARK GLASSMORPHISM)
                if not getattr(persistent, 'cm_bar_collapsed', True):
                    frame:
                        xsize 205
                        background "#0f141ee6"
                        padding (8, 8, 8, 8)
                        margin (0, 0, 0, 0)

                        vbox:
                            spacing 8
                            xsize 189

                            # --- NHÓM 1: NOVEL CONTROLS ---
                            vbox:
                                spacing 3
                                xsize 189
                                text _t("novel_controls") size 10 bold True color "#94a3b8"

                                # Lưới 2x2 nút điều khiển
                                vbox:
                                    spacing 4
                                    xsize 189
                                    hbox:
                                        spacing 4
                                        xsize 189
                                        button:
                                            action HideInterface()
                                            xsize 92
                                            ysize 28
                                            background "#ffffff14"
                                            hover_background "#ffffff29"
                                            text _t("hide_ui") size 11 bold True color "#f1f5f9" hover_color "#38bdf8" align (0.5, 0.5)

                                        $ is_skipping = bool(hasattr(renpy.config, 'skipping') and renpy.config.skipping)
                                        button:
                                            action Function(cheat_toggle_force_skip)
                                            xsize 92
                                            ysize 28
                                            background ("#0284c7" if is_skipping else "#ffffff14")
                                            hover_background ("#38bdf8" if is_skipping else "#ffffff29")
                                            text _t("skip") size 11 bold True color ("#ffffff" if is_skipping else "#f1f5f9") align (0.5, 0.5)

                                    hbox:
                                        spacing 4
                                        xsize 189
                                        $ is_auto = bool(getattr(_preferences, 'afm_time', 0) > 0 and getattr(_preferences, 'afm_enable', True))
                                        button:
                                            action Function(cheat_toggle_auto_forward)
                                            xsize 92
                                            ysize 28
                                            background ("#059669" if is_auto else "#ffffff14")
                                            hover_background ("#10b981" if is_auto else "#ffffff29")
                                            text _t("auto") size 11 bold True color ("#ffffff" if is_auto else "#f1f5f9") align (0.5, 0.5)

                                        button:
                                            action ToggleScreen("cheat_history_modal")
                                            xsize 92
                                            ysize 28
                                            background "#ffffff14"
                                            hover_background "#ffffff29"
                                            text _t("log") size 11 bold True color "#f1f5f9" hover_color "#38bdf8" align (0.5, 0.5)

                            # --- NHÓM 2: GAME DATA ---
                            vbox:
                                spacing 3
                                xsize 189
                                text _t("game_data") size 10 bold True color "#94a3b8"

                                vbox:
                                    spacing 4
                                    xsize 189
                                    hbox:
                                        spacing 4
                                        xsize 189
                                        button:
                                            action ShowMenu("save")
                                            xsize 92
                                            ysize 28
                                            background "#ffffff14"
                                            hover_background "#ffffff29"
                                            text _t("save") size 11 bold True color "#f1f5f9" hover_color "#fbbf24" align (0.5, 0.5)

                                        button:
                                            action ShowMenu("load")
                                            xsize 92
                                            ysize 28
                                            background "#ffffff14"
                                            hover_background "#ffffff29"
                                            text _t("load") size 11 bold True color "#f1f5f9" hover_color "#10b981" align (0.5, 0.5)

                                    hbox:
                                        spacing 4
                                        xsize 189
                                        button:
                                            action QuickSave()
                                            xsize 92
                                            ysize 28
                                            background "#ffffff14"
                                            hover_background "#ffffff29"
                                            text _t("q_save") size 11 bold True color "#f1f5f9" hover_color "#fbbf24" align (0.5, 0.5)

                                        button:
                                            action QuickLoad()
                                            xsize 92
                                            ysize 28
                                            background "#ffffff14"
                                            hover_background "#ffffff29"
                                            text _t("q_load") size 11 bold True color "#f1f5f9" hover_color "#10b981" align (0.5, 0.5)

                            # --- NHÓM 3: CHEAT ENGINE ---
                            vbox:
                                spacing 3
                                xsize 189
                                hbox:
                                    xsize 189
                                    yalign 0.5
                                    text _t("cheat_engine") size 10 bold True color "#94a3b8"
                                    hbox:
                                        xalign 1.0
                                        spacing 2
                                        textbutton "▲":
                                            action Function(cheat_nudge_bar_y, -50)
                                            text_size 9
                                            text_color "#64748b"
                                            text_hover_color "#38bdf8"
                                            padding (1, 0)
                                        textbutton "▼":
                                            action Function(cheat_nudge_bar_y, 50)
                                            text_size 9
                                            text_color "#64748b"
                                            text_hover_color "#38bdf8"
                                            padding (1, 0)

                                button:
                                    action ToggleScreen('cheat_main_modal')
                                    xsize 189
                                    ysize 30
                                    background "#0284c7"
                                    hover_background "#38bdf8"
                                    text _t("cheat_menu_btn") size 12 bold True color "#ffffff" align (0.5, 0.5)

                                if cheat_has_ai_trans():
                                    button:
                                        action [ToggleField(persistent, 'cm_auto_translate'), Function(renpy.restart_interaction)]
                                        xsize 189
                                        ysize 26
                                        background ("#059669" if persistent.cm_auto_translate else "#ffffff14")
                                        hover_background ("#10b981" if persistent.cm_auto_translate else "#ffffff29")
                                        if persistent.cm_auto_translate:
                                            text _t("ai_trans_on") size 11 bold True color "#ffffff" align (0.5, 0.5)
                                        else:
                                            text _t("ai_trans_off") size 11 bold True color "#94a3b8" hover_color "#f1f5f9" align (0.5, 0.5)

                                $ _w_mode = getattr(persistent, 'cm_wheel_fix_mode', 'off')
                                button:
                                    action Function(cheat_cycle_wheel_fix_mode)
                                    xsize 189
                                    ysize 26
                                    background ("#0284c7" if _w_mode == 'history' else ("#d97706" if _w_mode == 'disable' else "#ffffff14"))
                                    hover_background ("#38bdf8" if _w_mode == 'history' else ("#f59e0b" if _w_mode == 'disable' else "#ffffff29"))
                                    if _w_mode == 'history':
                                        text _t("wheel_log") size 11 bold True color "#ffffff" align (0.5, 0.5)
                                    elif _w_mode == 'disable':
                                        text _t("wheel_lock") size 11 bold True color "#ffffff" align (0.5, 0.5)
                                    else:
                                        text _t("wheel_default") size 11 color "#94a3b8" hover_color "#f1f5f9" align (0.5, 0.5)

# ==============================================================================
# SCREEN 2: BẢNG ĐIỀU KHIỂN CHEAT CHÍNH (PREMIUM DARK UI DASHBOARD)
# ==============================================================================
screen cheat_main_modal():
    modal True
    zorder 1100
    style_prefix "cheat"
    $ _t = cheat_tr

    # Chặn hoàn toàn con lăn chuột kích hoạt tính năng Rollback/Rollforward của game, đồng thời làm mới dữ liệu
    on "show" action Function(cheat_modal_on_show)
    on "hide" action Function(cheat_modal_on_hide)
    on "replace" action Function(cheat_modal_on_show)

    key "rollback" action NullAction()
    key "rollforward" action NullAction()

    # Lớp nền mờ tối dày toàn màn hình (chống lộ và chặn click vào giao diện quick_menu của game)
    add Solid("#040711f5")

    $ _cm_scale = cheat_get_ui_scale()
    $ _scale_pct = int(round(float(getattr(persistent, 'cm_ui_scale_user', 1.0) or 1.0) * 100))

    frame:
        at cheat_modal_scaler(_cm_scale)
        xsize 1040
        ysize 640
        background "#0b0f19fa"
        padding (20, 14)

        vbox:
            spacing 10

            # --- TOP HEADER ---
            hbox:
                xfill True
                yalign 0.5
                hbox:
                    spacing 8
                    yalign 0.5
                    text "⚡" size 22 color "#38bdf8"
                    text _t("title") size 18 bold True color "#f8fafc"

                hbox:
                    xalign 1.0
                    yalign 0.5
                    spacing 8

                    # Nút chọn ngôn ngữ trực quan (Language Selector Dropdown)
                    $ curr_lang = cheat_get_lang()
                    $ curr_lang_name = "English" if curr_lang == 'en' else u"Tiếng Việt"

                    button:
                        action ToggleField(cheat_menu_state, 'show_lang_dropdown')
                        background ("#0284c7" if getattr(cheat_menu_state, 'show_lang_dropdown', False) else "#1e293b")
                        hover_background "#38bdf8"
                        ysize 26
                        padding (8, 2)
                        yalign 0.5
                        hbox:
                            spacing 5
                            align (0.5, 0.5)
                            text "🌐" size 11 yalign 0.5
                            text "[curr_lang_name] ▼" size 11 bold True color "#ffffff" yalign 0.5

                    # Cụm điều khiển kích cỡ giao diện
                    hbox:
                        spacing 4
                        yalign 0.5
                        text _t("ui_size") size 11 color "#94a3b8" yalign 0.5
                        button:
                            action Function(cheat_step_ui_scale, -0.1)
                            background "#334155"
                            hover_background "#475569"
                            xsize 24
                            ysize 24
                            text "-" size 13 bold True color "#ffffff" align (0.5, 0.5)
                        button:
                            action Function(cheat_set_ui_scale, 1.0)
                            background "#1e293b"
                            hover_background "#334155"
                            ysize 24
                            padding (6, 0)
                            text "[_scale_pct]%" size 11 bold True color "#38bdf8" align (0.5, 0.5)
                        button:
                            action Function(cheat_step_ui_scale, 0.1)
                            background "#334155"
                            hover_background "#475569"
                            xsize 24
                            ysize 24
                            text "+" size 13 bold True color "#ffffff" align (0.5, 0.5)

                    button:
                        action Hide("cheat_main_modal")
                        background "#e11d48"
                        hover_background "#f43f5e"
                        padding (12, 5)
                        text _t("close") size 12 bold True color "#ffffff"

            # --- TAB NAVIGATION ---
            hbox:
                spacing 8
                button:
                    action [SetField(cheat_menu_state, 'current_tab', 'vars'), SetField(cheat_menu_state, 'show_lang_dropdown', False), Function(cheat_menu_state.invalidate_cache, False), Function(renpy.restart_interaction)]
                    background ("#0284c7" if cheat_menu_state.current_tab == 'vars' else "#1e293b")
                    hover_background "#0369a1"
                    padding (14, 8)
                    text _t("tab_vars") size 13 bold True color "#ffffff"

                button:
                    action [SetField(cheat_menu_state, 'current_tab', 'labels'), SetField(cheat_menu_state, 'show_lang_dropdown', False), Function(renpy.restart_interaction)]
                    background ("#0284c7" if cheat_menu_state.current_tab == 'labels' else "#1e293b")
                    hover_background "#0369a1"
                    padding (14, 8)
                    text _t("tab_labels") size 13 bold True color "#ffffff"

                button:
                    action [SetField(cheat_menu_state, 'current_tab', 'unlocks'), SetField(cheat_menu_state, 'show_lang_dropdown', False), Function(renpy.restart_interaction)]
                    background ("#0284c7" if cheat_menu_state.current_tab == 'unlocks' else "#1e293b")
                    hover_background "#0369a1"
                    padding (14, 8)
                    text _t("tab_unlocks") size 13 bold True color "#ffffff"

                if cheat_has_ai_trans():
                    button:
                        action [SetField(cheat_menu_state, 'current_tab', 'translate'), SetField(cheat_menu_state, 'show_lang_dropdown', False), Function(renpy.restart_interaction)]
                        background ("#0284c7" if cheat_menu_state.current_tab == 'translate' else "#1e293b")
                        hover_background "#0369a1"
                        padding (14, 8)
                        text _t("tab_translate") size 13 bold True color "#ffffff"

                button:
                    action [SetField(cheat_menu_state, 'current_tab', 'help'), SetField(cheat_menu_state, 'show_lang_dropdown', False), Function(renpy.restart_interaction)]
                    background ("#0284c7" if cheat_menu_state.current_tab == 'help' else "#1e293b")
                    hover_background "#0369a1"
                    padding (14, 8)
                    text _t("tab_help") size 13 bold True color "#ffffff"

            # ĐƯỜNG PHÂN CÁCH
            frame:
                xfill True
                ysize 1
                background "#334155"

            # ==================================================================
            # TAB 1: QUẢN LÝ BIẾN (VARIABLES)
            # ==================================================================
            if cheat_menu_state.current_tab == 'vars':
                $ paged_vars, total_vars, curr_p, max_p = cheat_menu_state.get_paged_vars()

                # THANH CÔNG CỤ LỌC & TÌM KIẾM
                hbox:
                    spacing 10
                    yalign 0.5
                    xfill True

                    # Bộ lọc loại
                    hbox:
                        spacing 5
                        yalign 0.5
                        text _t("filter") size 12 color "#94a3b8" yalign 0.5
                        button:
                            action [SetField(cheat_menu_state, 'var_filter_type', 'all'), Function(cheat_menu_state.invalidate_cache, True), Function(renpy.restart_interaction)]
                            background ("#0284c7" if cheat_menu_state.var_filter_type == 'all' else "#1e293b")
                            padding (7, 4)
                            text _t("filter_all") size 11 color "#ffffff"

                        button:
                            action [SetField(cheat_menu_state, 'var_filter_type', 'num'), Function(cheat_menu_state.invalidate_cache, True), Function(renpy.restart_interaction)]
                            background ("#0284c7" if cheat_menu_state.var_filter_type == 'num' else "#1e293b")
                            padding (7, 4)
                            text _t("filter_num") size 11 color "#ffffff"

                        button:
                            action [SetField(cheat_menu_state, 'var_filter_type', 'bool'), Function(cheat_menu_state.invalidate_cache, True), Function(renpy.restart_interaction)]
                            background ("#0284c7" if cheat_menu_state.var_filter_type == 'bool' else "#1e293b")
                            padding (7, 4)
                            text _t("filter_bool") size 11 color "#ffffff"

                        button:
                            action [SetField(cheat_menu_state, 'var_filter_type', 'str'), Function(cheat_menu_state.invalidate_cache, True), Function(renpy.restart_interaction)]
                            background ("#0284c7" if cheat_menu_state.var_filter_type == 'str' else "#1e293b")
                            padding (7, 4)
                            text _t("filter_str") size 11 color "#ffffff"

                    # Bước nhảy số
                    hbox:
                        spacing 4
                        yalign 0.5
                        text _t("step_val") size 12 color "#94a3b8" yalign 0.5
                        for step_val in [1, 10, 100, 1000]:
                            button:
                                action [SetField(cheat_menu_state, 'selected_amount', step_val), Function(renpy.restart_interaction)]
                                background ("#3b82f6" if cheat_menu_state.selected_amount == step_val else "#1e293b")
                                padding (6, 3)
                                $ s_lbl = str(step_val)
                                text "[s_lbl]" size 11 color "#ffffff"

                    # Thanh tìm kiếm biến & chỉ số game
                    hbox:
                        spacing 6
                        yalign 0.5
                        text _t("search_var") size 12 bold True color "#38bdf8" yalign 0.5
                        frame:
                            background "#090d16"
                            xsize 230
                            ysize 28
                            padding (6, 2)
                            yalign 0.5
                            hbox:
                                spacing 6
                                yalign 0.5
                                text _t("search_label") size 11 bold True color "#38bdf8" yalign 0.5
                                if cheat_menu_state.active_edit_var is None:
                                    input:
                                        value FieldInputValue(cheat_menu_state, 'search_var_keyword')
                                        length 25
                                        xsize 185
                                        copypaste True
                                        size 13
                                        bold True
                                        color "#ffffff"
                                        yalign 0.5
                                else:
                                    $ search_display = _safe_str(cheat_menu_state.search_var_keyword) if cheat_menu_state.search_var_keyword else _t("editing_num")
                                    text "[search_display!q]" size 12 color "#64748b" yalign 0.5

                        if cheat_menu_state.search_var_keyword:
                            button:
                                action [SetField(cheat_menu_state, 'search_var_keyword', ''), Function(cheat_menu_state.invalidate_cache, True), Function(renpy.restart_interaction)]
                                background "#ef4444"
                                hover_background "#f87171"
                                padding (6, 3)
                                yalign 0.5
                                text _t("clear") size 10 bold True color "#ffffff"

                    hbox:
                        xalign 1.0
                        yalign 0.5
                        spacing 8

                        button:
                            action [Function(cheat_menu_state.invalidate_cache, False), Function(cheat_notify, "notify_refresh"), Function(renpy.restart_interaction)]
                            background "#0284c7"
                            hover_background "#38bdf8"
                            padding (8, 4)
                            yalign 0.5
                            text _t("refresh") size 11 bold True color "#ffffff"

                        $ total_vars_lbl = _t("total_vars", total_vars)
                        text "[total_vars_lbl]" size 12 bold True color "#38bdf8" yalign 0.5

                # BẢNG HIỂN THỊ DANH SÁCH BIẾN THEO TRANG (KHÔNG DÙNG THANH CUỘN)
                vbox:
                    spacing 6
                    ysize 400
                    if not paged_vars:
                        frame:
                            xfill True
                            background "#1e293b44"
                            padding (20, 20)
                            text _t("no_vars_found") size 13 color "#94a3b8" xalign 0.5
                    else:
                        for item in paged_vars:
                                $ v_name = item[0]
                                $ live_val = _cheat_get_nested_val(v_name, _CHEAT_NOT_FOUND)
                                $ v_val = live_val if live_val is not _CHEAT_NOT_FOUND else item[1]
                                $ v_type = item[2]
                                $ is_frozen = item[3]
                                $ is_pinned = item[4]

                                frame:
                                    xfill True
                                    background ("#1e293b99" if not is_pinned else "#0369a133")
                                    padding (10, 6)

                                    hbox:
                                        spacing 10
                                        yalign 0.5

                                        # Nút Ghim (Pin)
                                        button:
                                            action Function(cheat_menu_state.toggle_pin, v_name)
                                            background ("#f59e0b" if is_pinned else "#334155")
                                            hover_background "#d97706"
                                            xsize 26
                                            ysize 26
                                            padding (0, 0)
                                            text ("*" if is_pinned else "+") size 12 bold True color "#ffffff" align (0.5, 0.5)

                                        # Nút Đóng băng (Freeze)
                                        button:
                                            action Function(cheat_menu_state.toggle_freeze, v_name)
                                            background ("#06b6d4" if is_frozen else "#334155")
                                            hover_background "#0891b2"
                                            ysize 26
                                            padding (8, 0)
                                            text (_t("locked") if is_frozen else _t("lock")) size 10 bold True color "#ffffff" align (0.5, 0.5)

                                        # Badge loại dữ liệu
                                        frame:
                                            background ("#0284c7" if v_type == 'num' else ("#059669" if v_type == 'bool' else ("#d97706" if v_type == 'str' else "#475569")))
                                            padding (6, 2)
                                            $ badge_lbl = "NUM" if v_type == 'num' else ("BOOL" if v_type == 'bool' else ("STR" if v_type == 'str' else "OBJ"))
                                            text "[badge_lbl]" size 10 bold True color "#ffffff"

                                        # Tên biến
                                        $ display_name = _safe_str(v_name)
                                        text "[display_name!q]" size 13 bold True color ("#38bdf8" if is_pinned else "#f1f5f9") xsize 230

                                        # Cột hiển thị giá trị
                                        $ display_val = _safe_str(v_val)
                                        if v_type == 'num':
                                            if cheat_menu_state.active_edit_var == v_name:
                                                # Đang nhập trực tiếp trong ô: font size chuẩn 13, bắt buộc focus bàn phím
                                                frame:
                                                    xsize 130
                                                    ysize 28
                                                    background "#0369a1"
                                                    padding (4, 2)
                                                    yalign 0.5
                                                    input:
                                                        value FieldInputValue(cheat_menu_state, 'input_val')
                                                        allow "0123456789.-"
                                                        length 14
                                                        copypaste True
                                                        default True
                                                        size 13
                                                        bold True
                                                        color "#ffffff"
                                                        yalign 0.5
                                                button:
                                                    action Function(cheat_menu_state.apply_input_val)
                                                    background "#10b981"
                                                    hover_background "#059669"
                                                    ysize 26
                                                    padding (8, 0)
                                                    yalign 0.5
                                                    text _t("save") size 11 bold True color "#ffffff" align (0.5, 0.5)
                                                button:
                                                    action Function(cheat_menu_state.cancel_editor)
                                                    background "#e11d48"
                                                    hover_background "#f43f5e"
                                                    ysize 26
                                                    padding (8, 0)
                                                    yalign 0.5
                                                    text _t("cancel") size 11 bold True color "#ffffff" align (0.5, 0.5)
                                            else:
                                                # Click vào số để nhập trực tiếp bằng bàn phím
                                                button:
                                                    action Function(cheat_menu_state.open_number_editor, v_name, v_val)
                                                    background "#1e293b"
                                                    hover_background "#0284c7"
                                                    padding (6, 3)
                                                    xsize 170
                                                    ysize 26
                                                    $ preview_num = cheat_truncate_single_line(display_val, 16)
                                                    text "[preview_num!q]" size 13 bold True color "#4ade80" yalign 0.5 layout "nobreak"

                                        elif v_type == 'str':
                                            if cheat_menu_state.active_edit_var == v_name:
                                                # Đang nhập trực tiếp chuỗi chữ: font size 13, cho phép nhập bất kỳ văn bản/ký tự nào
                                                frame:
                                                    xsize 130
                                                    ysize 28
                                                    background "#b45309"
                                                    padding (4, 2)
                                                    yalign 0.5
                                                    input:
                                                        value FieldInputValue(cheat_menu_state, 'input_val')
                                                        length 45
                                                        copypaste True
                                                        default True
                                                        size 13
                                                        bold True
                                                        color "#ffffff"
                                                        yalign 0.5
                                                button:
                                                    action Function(cheat_menu_state.apply_input_val)
                                                    background "#10b981"
                                                    hover_background "#059669"
                                                    ysize 26
                                                    padding (8, 0)
                                                    yalign 0.5
                                                    text _t("save") size 11 bold True color "#ffffff" align (0.5, 0.5)
                                                button:
                                                    action Function(cheat_menu_state.cancel_editor)
                                                    background "#e11d48"
                                                    hover_background "#f43f5e"
                                                    ysize 26
                                                    padding (8, 0)
                                                    yalign 0.5
                                                    text _t("cancel") size 11 bold True color "#ffffff" align (0.5, 0.5)
                                            else:
                                                # Click vào chữ để sửa trực tiếp bằng bàn phím y như Stats
                                                button:
                                                    action Function(cheat_menu_state.open_str_editor, v_name, v_val)
                                                    background "#1e293b"
                                                    hover_background "#d97706"
                                                    padding (6, 3)
                                                    xsize 170
                                                    ysize 26
                                                    $ preview_str = cheat_truncate_single_line(display_val, 16) if display_val else _t("empty_str")
                                                    text "[preview_str!q]" size 13 bold True color ("#f59e0b" if display_val else "#64748b") yalign 0.5 layout "nobreak"

                                        else:
                                            # Cờ (Bool) hoặc đối tượng khác
                                            $ preview_other = cheat_truncate_single_line(display_val, 16)
                                            text "[preview_other!q]" size 13 color "#94a3b8" xsize 170 yalign 0.5 layout "nobreak"

                                        # Các thao tác sửa giá trị
                                        if v_type == 'num':
                                            $ cur_step = cheat_menu_state.selected_amount
                                            $ minus_lbl = "-%d" % cur_step
                                            $ plus_lbl = "+%d" % cur_step
                                            button:
                                                action Function(cheat_menu_state.step_val, v_name, -cur_step)
                                                background "#334155"
                                                hover_background "#ef4444"
                                                ysize 26
                                                padding (8, 0)
                                                text "[minus_lbl]" size 11 color "#ffffff" align (0.5, 0.5)

                                            button:
                                                action Function(cheat_menu_state.step_val, v_name, cur_step)
                                                background "#334155"
                                                hover_background "#10b981"
                                                ysize 26
                                                padding (8, 0)
                                                text "[plus_lbl]" size 11 color "#ffffff" align (0.5, 0.5)

                                            button:
                                                action Function(cheat_set_max_val, v_name)
                                                background "#0284c7"
                                                hover_background "#38bdf8"
                                                ysize 26
                                                padding (8, 0)
                                                text "MAX" size 11 bold True color "#ffffff" align (0.5, 0.5)

                                            button:
                                                action Function(cheat_menu_state.set_val, v_name, 0)
                                                background "#475569"
                                                hover_background "#64748b"
                                                ysize 26
                                                padding (8, 0)
                                                text "0" size 11 color "#ffffff" align (0.5, 0.5)

                                        elif v_type == 'bool':
                                            button:
                                                action Function(cheat_menu_state.toggle_bool, v_name)
                                                background ("#059669" if v_val else "#e11d48")
                                                hover_background ("#10b981" if v_val else "#f43f5e")
                                                ysize 26
                                                padding (14, 0)
                                                text (_t("bool_true") if v_val else _t("bool_false")) size 11 bold True color "#ffffff" align (0.5, 0.5)

                                        elif v_type == 'str':
                                            button:
                                                action Function(cheat_menu_state.open_str_editor, v_name, v_val)
                                                background "#d97706"
                                                hover_background "#f59e0b"
                                                ysize 26
                                                padding (10, 0)
                                                text _t("edit_str") size 11 bold True color "#ffffff" align (0.5, 0.5)

                                            button:
                                                action Function(cheat_menu_state.set_val, v_name, "")
                                                background "#475569"
                                                hover_background "#ef4444"
                                                ysize 26
                                                padding (8, 0)
                                                text _t("clear_str") size 11 color "#ffffff" align (0.5, 0.5)

                                        else:
                                            text _t("game_object") size 11 color "#64748b"

                # THANH ĐIỀU HƯỚNG PHÂN TRANG (NHƯ CŨ - KHÔNG DÙNG THANH CUỘN)
                hbox:
                    spacing 16
                    xalign 0.5
                    yalign 0.5
                    button:
                        action Function(cheat_menu_state.prev_page)
                        background ("#0284c7" if curr_p > 1 else "#334155")
                        hover_background ("#38bdf8" if curr_p > 1 else "#334155")
                        ysize 30
                        padding (14, 0)
                        text _t("page_prev") size 12 bold True color "#ffffff" align (0.5, 0.5)

                    $ page_info = _t("page_info_vars", curr_p, max_p, total_vars)
                    text "[page_info]" size 13 bold True color "#38bdf8" yalign 0.5

                    button:
                        action Function(cheat_menu_state.next_page)
                        background ("#0284c7" if curr_p < max_p else "#334155")
                        hover_background ("#38bdf8" if curr_p < max_p else "#334155")
                        ysize 30
                        padding (14, 0)
                        text _t("page_next") size 12 bold True color "#ffffff" align (0.5, 0.5)

            # ==================================================================
            # TAB 2: NHẢY CẢNH (LABELS JUMPER)
            # ==================================================================
            elif cheat_menu_state.current_tab == 'labels':
                $ paged_lbls, total_lbl_count, curr_lp, max_lp = cheat_menu_state.get_paged_labels()

                hbox:
                    xfill True
                    yalign 0.5
                    hbox:
                        spacing 8
                        yalign 0.5
                        text _t("search_scene") size 13 bold True color "#38bdf8" yalign 0.5
                        frame:
                            background "#090d16"
                            xsize 300
                            ysize 28
                            padding (6, 2)
                            yalign 0.5
                            hbox:
                                spacing 6
                                yalign 0.5
                                text _t("search_label") size 11 bold True color "#38bdf8" yalign 0.5
                                input:
                                    value FieldInputValue(cheat_menu_state, 'search_label_keyword')
                                    length 30
                                    xsize 250
                                    copypaste True
                                    size 13
                                    bold True
                                    color "#ffffff"
                                    yalign 0.5

                        if cheat_menu_state.search_label_keyword:
                            button:
                                action [SetField(cheat_menu_state, 'search_label_keyword', ''), Function(cheat_menu_state.invalidate_cache, True), Function(renpy.restart_interaction)]
                                background "#ef4444"
                                hover_background "#f87171"
                                ysize 26
                                padding (8, 0)
                                yalign 0.5
                                text _t("clear") size 11 bold True color "#ffffff" align (0.5, 0.5)

                    $ total_lbls_lbl = _t("total_labels", total_lbl_count)
                    text "[total_lbls_lbl]" size 12 bold True color "#38bdf8" xalign 1.0 yalign 0.5

                vbox:
                    spacing 5
                    ysize 400
                    if not paged_lbls:
                        frame:
                            xfill True
                            background "#1e293b44"
                            padding (20, 20)
                            text _t("no_labels_found") size 13 color "#94a3b8" xalign 0.5
                    else:
                        for lbl in paged_lbls:
                            frame:
                                xfill True
                                background "#1e293b77"
                                padding (10, 5)

                                hbox:
                                    spacing 12
                                    yalign 0.5
                                    $ lbl_str = _safe_str(lbl)
                                    text "[lbl_str!q]" size 13 color "#f1f5f9" xsize 550

                                    button:
                                        action Function(cheat_safe_jump, lbl)
                                        background "#0284c7"
                                        hover_background "#38bdf8"
                                        ysize 26
                                        padding (12, 0)
                                        text _t("jump_btn") size 12 bold True color "#ffffff" align (0.5, 0.5)

                                    button:
                                        action Function(cheat_safe_call, lbl)
                                        background "#059669"
                                        hover_background "#10b981"
                                        ysize 26
                                        padding (12, 0)
                                        text _t("call_btn") size 12 bold True color "#ffffff" align (0.5, 0.5)

                # THANH ĐIỀU HƯỚNG PHÂN TRANG LABELS (NHƯ CŨ - KHÔNG DÙNG THANH CUỘN)
                hbox:
                    spacing 16
                    xalign 0.5
                    yalign 0.5
                    button:
                        action Function(cheat_menu_state.prev_label_page)
                        background ("#0284c7" if curr_lp > 1 else "#334155")
                        hover_background ("#38bdf8" if curr_lp > 1 else "#334155")
                        ysize 30
                        padding (14, 0)
                        text _t("page_prev") size 12 bold True color "#ffffff" align (0.5, 0.5)

                    $ lbl_page_info = _t("page_info_labels", curr_lp, max_lp, total_lbl_count)
                    text "[lbl_page_info]" size 13 bold True color "#38bdf8" yalign 0.5

                    button:
                        action Function(cheat_menu_state.next_label_page)
                        background ("#0284c7" if curr_lp < max_lp else "#334155")
                        hover_background ("#38bdf8" if curr_lp < max_lp else "#334155")
                        ysize 30
                        padding (14, 0)
                        text _t("page_next") size 12 bold True color "#ffffff" align (0.5, 0.5)

            # ==================================================================
            # TAB 3: MỞ KHÓA & HỆ THỐNG (UNLOCKS & SYSTEM)
            # ==================================================================
            elif cheat_menu_state.current_tab == 'unlocks':
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    ysize 470
                    xfill True
                    vbox:
                        spacing 14
                        xfill True

                        # Card Cài đặt ngôn ngữ (Language Settings Card)
                        frame:
                            xfill True
                            background "#1e293b88"
                            padding (16, 14)
                            vbox:
                                spacing 8
                                text _t("lang_section_title") size 16 bold True color "#38bdf8"
                                text _t("lang_section_desc") size 12 color "#94a3b8"
                                hbox:
                                    spacing 10
                                    for l_code, l_name, l_badge in CHEAT_LANGUAGES:
                                        $ is_l_active = (cheat_get_lang() == l_code)
                                        button:
                                            action Function(cheat_set_lang, l_code)
                                            background ("#0284c7" if is_l_active else "#334155")
                                            hover_background ("#0369a1" if is_l_active else "#475569")
                                            ysize 32
                                            padding (16, 0)
                                            hbox:
                                                spacing 8
                                                align (0.5, 0.5)
                                                text "[l_badge]" size 11 bold True color ("#ffffff" if is_l_active else "#94a3b8") yalign 0.5
                                                text "[l_name]" size 12 bold is_l_active color ("#ffffff" if is_l_active else "#cbd5e1") yalign 0.5
                                                if is_l_active:
                                                    text "✓" size 13 bold True color "#4ade80" yalign 0.5

                        frame:
                            xfill True
                            background "#1e293b88"
                            padding (16, 14)
                            vbox:
                                spacing 8
                                text _t("gallery_title") size 16 bold True color "#38bdf8"
                                text _t("gallery_desc") size 12 color "#94a3b8"
                                button:
                                    action Function(cheat_unlock_all_gallery)
                                    background "#0284c7"
                                    hover_background "#38bdf8"
                                    ysize 32
                                    padding (14, 0)
                                    text _t("gallery_btn") size 13 bold True color "#ffffff" align (0.5, 0.5)

                        frame:
                            xfill True
                            background "#1e293b88"
                            padding (16, 14)
                            vbox:
                                spacing 8
                                text _t("dev_title") size 16 bold True color "#38bdf8"
                                text _t("dev_desc") size 12 color "#94a3b8"
                                hbox:
                                    spacing 12
                                    yalign 0.5
                                    text (_t("dev_active") if getattr(config, 'developer', False) else _t("dev_inactive")) size 13 bold True color ("#10b981" if getattr(config, 'developer', False) else "#ef4444")
                                    if not getattr(config, 'developer', False):
                                        button:
                                            action Function(cheat_enable_developer)
                                            background "#10b981"
                                            hover_background "#059669"
                                            ysize 26
                                            padding (10, 0)
                                            text _t("dev_btn") size 12 color "#ffffff" align (0.5, 0.5)

                        frame:
                            xfill True
                            background "#1e293b88"
                            padding (16, 14)
                            vbox:
                                spacing 8
                                text _t("skip_title") size 16 bold True color "#38bdf8"
                                text _t("skip_desc") size 12 color "#94a3b8"
                                button:
                                    action Function(cheat_enable_force_skip_permanent)
                                    background "#059669"
                                    hover_background "#10b981"
                                    ysize 28
                                    padding (12, 0)
                                    text _t("skip_btn") size 12 bold True color "#ffffff" align (0.5, 0.5)

                        frame:
                            xfill True
                            background "#1e293b88"
                            padding (16, 14)
                            vbox:
                                spacing 8
                                text _t("wheel_title") size 16 bold True color "#38bdf8"
                                text _t("wheel_desc") size 12 color "#94a3b8"

                                $ curr_wf = getattr(persistent, 'cm_wheel_fix_mode', 'off')
                                $ curr_dr = getattr(persistent, 'cm_disable_rollback', False)

                                hbox:
                                    spacing 10
                                    yalign 0.5
                                    text _t("wheel_mode") size 13 bold True color "#f1f5f9"
                                    if curr_wf == 'history':
                                        text _t("wheel_active_log") size 12 bold True color "#10b981"
                                    elif curr_wf == 'disable':
                                        text _t("wheel_active_lock") size 12 bold True color "#f59e0b"
                                    else:
                                        text _t("wheel_active_off") size 12 color "#94a3b8"

                                hbox:
                                    spacing 8
                                    button:
                                        action Function(cheat_set_wheel_fix_mode, 'history')
                                        background ("#0284c7" if curr_wf == 'history' else "#334155")
                                        hover_background ("#38bdf8" if curr_wf == 'history' else "#475569")
                                        ysize 30
                                        padding (12, 0)
                                        text _t("wheel_opt1") size 11 bold True color "#ffffff" align (0.5, 0.5)

                                    button:
                                        action Function(cheat_set_wheel_fix_mode, 'disable')
                                        background ("#d97706" if curr_wf == 'disable' else "#334155")
                                        hover_background ("#f59e0b" if curr_wf == 'disable' else "#475569")
                                        ysize 30
                                        padding (12, 0)
                                        text _t("wheel_opt2") size 11 bold True color "#ffffff" align (0.5, 0.5)

                                    button:
                                        action Function(cheat_set_wheel_fix_mode, 'off')
                                        background ("#475569" if curr_wf == 'off' else "#1e293b")
                                        hover_background "#64748b"
                                        ysize 30
                                        padding (12, 0)
                                        text _t("wheel_opt3") size 11 color "#ffffff" align (0.5, 0.5)

                                hbox:
                                    spacing 10
                                    yalign 0.5
                                    text _t("rollback_lock_label") size 12 color "#cbd5e1"
                                    button:
                                        action Function(cheat_toggle_disable_rollback)
                                        background ("#e11d48" if curr_dr else "#334155")
                                        hover_background ("#f43f5e" if curr_dr else "#475569")
                                        ysize 26
                                        padding (10, 0)
                                        text (_t("rollback_locked") if curr_dr else _t("rollback_unlocked")) size 11 bold True color "#ffffff" align (0.5, 0.5)

                                hbox:
                                    spacing 10
                                    yalign 0.5
                                    text _t("single_key_label") size 12 color "#cbd5e1"
                                    $ curr_sks = getattr(persistent, 'cm_single_key_shortcuts', True)
                                    button:
                                        action [ToggleField(persistent, 'cm_single_key_shortcuts'), Function(renpy.restart_interaction)]
                                        background ("#0284c7" if curr_sks else "#334155")
                                        hover_background ("#38bdf8" if curr_sks else "#475569")
                                        ysize 26
                                        padding (10, 0)
                                        text (_t("single_key_on") if curr_sks else _t("single_key_off")) size 11 bold True color "#ffffff" align (0.5, 0.5)

                        frame:
                            xfill True
                            background "#1e293b88"
                            padding (16, 14)
                            vbox:
                                spacing 8
                                text _t("recovery_title") size 16 bold True color "#38bdf8"
                                text _t("recovery_desc") size 12 color "#94a3b8"
                                hbox:
                                    spacing 12
                                    yalign 0.5
                                    $ curr_rec = getattr(persistent, 'cm_auto_recover_crash', True)
                                    text (_t("recovery_status_on") if curr_rec else _t("recovery_status_off")) size 13 bold True color ("#10b981" if curr_rec else "#ef4444")
                                    button:
                                        action [ToggleField(persistent, 'cm_auto_recover_crash'), Function(renpy.restart_interaction)]
                                        background ("#059669" if curr_rec else "#e11d48")
                                        hover_background ("#10b981" if curr_rec else "#f43f5e")
                                        ysize 26
                                        padding (12, 0)
                                        text (_t("recovery_btn_on") if curr_rec else _t("recovery_btn_off")) size 12 bold True color "#ffffff" align (0.5, 0.5)

                        frame:
                            xfill True
                            background "#1e293b88"
                            padding (16, 14)
                            vbox:
                                spacing 8
                                text _t("sync_games_title") size 16 bold True color "#38bdf8"
                                text _t("sync_games_desc") size 12 color "#94a3b8"
                                button:
                                    action Function(cheat_sync_all_games)
                                    background "#8b5cf6"
                                    hover_background "#a78bfa"
                                    ysize 32
                                    padding (16, 0)
                                    text _t("sync_games_btn") size 13 bold True color "#ffffff" align (0.5, 0.5)

            # ==================================================================
            # TAB 4: DỊCH THUẬT (AUTO-TRANSLATE EN -> VI)
            # ==================================================================
            elif cheat_menu_state.current_tab == 'translate':
                if renpy.has_screen('cheat_translate_panel'):
                    use expression "cheat_translate_panel"
                else:
                    vbox:
                        spacing 16
                        ysize 470
                        frame:
                            xfill True
                            background "#ef444422"
                            padding (24, 20)
                            vbox:
                                spacing 10
                                text _t("trans_not_active") size 18 bold True color "#ef4444"
                                text _t("trans_info1") size 13 color "#f8fafc"
                                text _t("trans_info2") size 12 color "#94a3b8"

                        frame:
                            xfill True
                            background "#1e293b88"
                            padding (20, 16)
                            vbox:
                                spacing 8
                                text _t("trans_guide_title") size 14 bold True color "#38bdf8"
                                text _t("trans_guide1") size 12 color "#cbd5e1"
                                text _t("trans_guide2") size 12 color "#cbd5e1"
                                text _t("trans_guide3") size 12 color "#cbd5e1"

            # ==================================================================
            # TAB 5: PHÍM TẮT & TRỢ GIÚP
            # ==================================================================
            elif cheat_menu_state.current_tab == 'help':
                vbox:
                    spacing 10
                    ysize 470

                    text _t("hotkeys_title") size 15 bold True color "#38bdf8"

                    grid 2 10:
                        spacing 5
                        text _t("hk_menu_key") size 12 color "#f1f5f9"
                        text _t("hk_menu_desc") size 12 color "#94a3b8"

                        text _t("hk_star_key") size 12 color "#f1f5f9"
                        text _t("hk_star_desc") size 12 color "#94a3b8"

                        text _t("hk_alt_star_key") size 12 color "#f1f5f9"
                        text _t("hk_alt_star_desc") size 12 color "#94a3b8"

                        text _t("hk_h_key") size 12 color "#f1f5f9"
                        text _t("hk_h_desc") size 12 color "#94a3b8"

                        text _t("hk_s_key") size 12 color "#f1f5f9"
                        text _t("hk_s_desc") size 12 color "#94a3b8"

                        text _t("hk_a_key") size 12 color "#f1f5f9"
                        text _t("hk_a_desc") size 12 color "#94a3b8"

                        text _t("hk_l_key") size 12 color "#f1f5f9"
                        text _t("hk_l_desc") size 12 color "#94a3b8"

                        text _t("hk_dev_key") size 12 color "#f1f5f9"
                        text _t("hk_dev_desc") size 12 color "#94a3b8"

                        text _t("hk_cloud_key") size 12 color "#f1f5f9"
                        text _t("hk_cloud_desc") size 12 color "#94a3b8"

                        text _t("hk_wheel_key") size 12 color "#f1f5f9"
                        text _t("hk_wheel_desc") size 12 color "#94a3b8"

                    frame:
                        xfill True
                        background "#0f172ae6"
                        padding (12, 8)
                        vbox:
                            spacing 6
                            hbox:
                                spacing 8
                                yalign 0.5
                                text _t("scaling_title") size 12 bold True color "#38bdf8"
                                $ curr_res_txt = "%dx%d" % (int(config.screen_width), int(config.screen_height))
                                text _t("game_res", curr_res_txt) size 11 color "#94a3b8" yalign 0.5

                            text _t("scaling_desc") size 11 color "#cbd5e1"

                            hbox:
                                spacing 6
                                yalign 0.5
                                text "Preset:" size 11 color "#94a3b8" yalign 0.5
                                for p_val, p_lbl in [(0.8, "80%"), (0.9, "90%"), (1.0, "100%"), (1.1, "110%"), (1.2, "120%"), (1.3, "130%")]:
                                    $ is_p_act = (abs(float(getattr(persistent, 'cm_ui_scale_user', 1.0) or 1.0) - p_val) < 0.04)
                                    button:
                                        action Function(cheat_set_ui_scale, p_val)
                                        background ("#0284c7" if is_p_act else "#1e293b")
                                        hover_background ("#0369a1" if is_p_act else "#334155")
                                        ysize 24
                                        padding (8, 0)
                                        text "[p_lbl]" size 10 bold is_p_act color ("#ffffff" if is_p_act else "#94a3b8") align (0.5, 0.5)

                    frame:
                        xfill True
                        background "#1e293b66"
                        padding (12, 8)
                        text _t("tip_pinned") size 11 color "#fbbf24"

    # Menu danh sách chọn ngôn ngữ dạng Dropdown Popover (Language Dropdown)
    if getattr(cheat_menu_state, 'show_lang_dropdown', False):
        frame:
            at cheat_modal_scaler(_cm_scale)
            align (0.5, 0.5)
            xsize 380
            ysize 240
            background "#0f172af8"
            padding (18, 16)

            vbox:
                spacing 12
                xfill True
                yfill True

                hbox:
                    xfill True
                    yalign 0.5
                    text _t("select_language") size 15 bold True color "#38bdf8"
                    textbutton "✕":
                        action SetField(cheat_menu_state, 'show_lang_dropdown', False)
                        text_size 15
                        text_color "#94a3b8"
                        text_hover_color "#f43f5e"

                frame:
                    xfill True
                    ysize 1
                    background "#334155"

                vbox:
                    spacing 8
                    xfill True
                    for l_code, l_name, l_badge in CHEAT_LANGUAGES:
                        $ is_l_active = (cheat_get_lang() == l_code)
                        button:
                            action [Function(cheat_set_lang, l_code), SetField(cheat_menu_state, 'show_lang_dropdown', False)]
                            xfill True
                            ysize 42
                            background ("#0284c7" if is_l_active else "#1e293b")
                            hover_background ("#0369a1" if is_l_active else "#334155")
                            padding (14, 8)
                            hbox:
                                spacing 12
                                yalign 0.5
                                text "[l_badge]" size 12 bold True color ("#ffffff" if is_l_active else "#94a3b8") yalign 0.5
                                text "[l_name]" size 13 bold is_l_active color ("#ffffff" if is_l_active else "#cbd5e1") yalign 0.5
                                if is_l_active:
                                    text "✓" size 14 bold True color "#4ade80" xalign 1.0 yalign 0.5

    # Phím tắt xác nhận khi đang nhập số hoặc sửa bản dịch
    if cheat_menu_state.active_edit_var is not None:
        key "K_RETURN" action Function(cheat_menu_state.apply_input_val)
        key "K_KP_ENTER" action Function(cheat_menu_state.apply_input_val)
        key "K_ESCAPE" action Function(cheat_menu_state.cancel_editor)

    $ct_st = getattr(renpy.store, 'cheat_trans_state', None)
    if ct_st and getattr(ct_st, 'active_edit_trans_orig', None) is not None:
        key "K_RETURN" action Function(ct_st.apply_trans_edit)
        key "K_KP_ENTER" action Function(ct_st.apply_trans_edit)
        key "K_ESCAPE" action Function(ct_st.cancel_trans_editor)
    elif cheat_menu_state.active_edit_trans_orig is not None:
        key "K_RETURN" action Function(cheat_menu_state.apply_trans_edit)
        key "K_KP_ENTER" action Function(cheat_menu_state.apply_trans_edit)
        key "K_ESCAPE" action Function(cheat_menu_state.cancel_trans_editor)

# ==============================================================================
# SCREEN 3: NHẬT KÝ HỘI THOẠI & ĐIỂM QUAY LẠI TƯƠNG TÁC (INTERACTIVE HISTORY LOG)
# ==============================================================================
screen cheat_history_modal():
    modal True
    zorder 1200
    style_prefix "cheat"
    $ _t = cheat_tr

    key "K_ESCAPE" action Hide("cheat_history_modal")
    key "l" action Hide("cheat_history_modal")
    key "L" action Hide("cheat_history_modal")

    # Nền mờ tối chống click lọt ra game
    add Solid("#040711ee")

    $ _cm_scale = cheat_get_ui_scale()
    $ hist_list = cheat_get_history_entries()
    $ total_hist = len(hist_list)

    frame:
        at cheat_modal_scaler(_cm_scale)
        xsize 1040
        ysize 640
        background "#0b0f19fa"
        padding (20, 16)
        align (0.5, 0.5)

        vbox:
            spacing 10
            xfill True
            yfill True

            # --- HEADER ---
            hbox:
                xfill True
                yalign 0.5
                vbox:
                    spacing 3
                    hbox:
                        spacing 8
                        yalign 0.5
                        text _t("hist_title") size 16 bold True color "#f8fafc"
                        $ hist_count_txt = _t("hist_count", total_hist)
                        text "[hist_count_txt]" size 12 bold True color "#38bdf8" yalign 0.5
                    text _t("hist_desc") size 11 color "#94a3b8"

                hbox:
                    xalign 1.0
                    yalign 0.5
                    spacing 8
                    button:
                        action Hide("cheat_history_modal")
                        background "#e11d48"
                        hover_background "#f43f5e"
                        padding (14, 6)
                        text _t("close") size 12 bold True color "#ffffff"

            # ĐƯỜNG PHÂN CÁCH
            frame:
                xfill True
                ysize 1
                background "#334155"

            # --- DANH SÁCH LỊCH SỬ HỘI THOẠI ---
            if total_hist == 0:
                vbox:
                    xfill True
                    yfill True
                    align (0.5, 0.5)
                    spacing 8
                    text _t("hist_empty_title") size 15 bold True color "#94a3b8" align (0.5, 0.5)
                    text _t("hist_empty_desc") size 12 color "#64748b" align (0.5, 0.5)
            else:
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    yinitial 1.0
                    xfill True
                    ysize 490

                    vbox:
                        spacing 8
                        xfill True

                        for idx, h in enumerate(hist_list):
                            $ steps_back = total_hist - 1 - idx
                            $ h_who = getattr(h, 'who', None)
                            $ h_what = getattr(h, 'what', "") or ""
                            $ who_color = "#38bdf8"
                            if getattr(h, 'who_args', None) and isinstance(h.who_args, dict) and 'color' in h.who_args:
                                $ who_color = h.who_args['color']

                            frame:
                                xfill True
                                background "#1e293b66"
                                hover_background "#1e293bcc"
                                padding (12, 8)

                                hbox:
                                    xfill True
                                    spacing 12
                                    yalign 0.5

                                    # Bấm vào toàn bộ nội dung để quay lại
                                    button:
                                        action Function(cheat_rollback_to_history, h, steps_back)
                                        xsize 850
                                        background None
                                        hover_background None
                                        padding (0, 0)

                                        vbox:
                                            spacing 3
                                            xfill True
                                            if h_who:
                                                text h_who size 12 bold True color who_color substitute False
                                            text h_what size 12 color "#f1f5f9" substitute False

                                    # Nút bấm riêng biệt
                                    button:
                                        action Function(cheat_rollback_to_history, h, steps_back)
                                        xalign 1.0
                                        yalign 0.5
                                        background "#0284c7"
                                        hover_background "#38bdf8"
                                        padding (10, 5)
                                        xsize 100
                                        text _t("hist_restore") size 11 bold True color "#ffffff" align (0.5, 0.5)

            # --- FOOTER ---
            hbox:
                xfill True
                yalign 0.5
                text _t("hist_footer_tip") size 11 color "#64748b"
                hbox:
                    xalign 1.0
                    spacing 8
                    button:
                        action [Hide("cheat_history_modal"), ShowMenu("history")]
                        background "#334155"
                        hover_background "#475569"
                        padding (8, 4)
                        text _t("hist_open_game") size 11 color "#cbd5e1"

# ==============================================================================
# BẢO VỆ CẤU HÌNH STYLE LẦN CUỐI SAU KHI GAME LOAD XONG (POST-INIT IMMUNITY)
# ==============================================================================
init 999 python:
    cheat_setup_isolated_styles()
    cheat_apply_wheel_protection()

