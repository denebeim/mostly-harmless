import Gio from 'gi://Gio';
import Clutter from 'gi://Clutter';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';
const XML = `<node><interface name="org.gnome.Shell.Extensions.GeminiFocus">
<method name="Focus"><arg type="s" direction="out"/></method>
<method name="Send"><arg type="s" direction="in"/><arg type="s" direction="out"/></method>
<method name="Status"><arg type="s" direction="out"/></method>
</interface></node>`;
export default class GeminiFocus extends Extension {
    enable() {
        this._keyboard = global.stage.context.get_backend().get_default_seat().create_virtual_device(Clutter.InputDeviceType.KEYBOARD_DEVICE);
        this._object = Gio.DBusExportedObject.wrapJSObject(XML, this);
        this._object.export(Gio.DBus.session, '/org/gnome/Shell/Extensions/GeminiFocus');
    }
    disable() { this._object?.unexport(); this._object = null; this._keyboard = null; }
    _windows() {
        if (Main.sessionMode.isLocked) return [];
        return global.get_window_actors().map(a => a.meta_window).filter(w => {
            const title = w.get_title() ?? '';
            const cls = w.get_wm_class() ?? '';
            return /^chrome-gemini\.google\.com__/i.test(cls) &&
                (/^Google Gemini(?: -|$)/.test(title) || / - Google Gemini(?: -|$)/.test(title));
        });
    }
    Focus() {
        if (Main.sessionMode.isLocked) return 'locked';
        const windows = this._windows();
        const focused = global.display.focus_window;
        const w = windows.includes(focused) ? focused : windows[0];
        if (!w) return 'missing';
        if (focused === w && !Main.overview.visible) return 'focused';
        Main.overview.hide();
        Main.activateWindow(w, global.get_current_time());
        return 'pending';
    }
    Send(action) {
        if (!['dictate', 'submit'].includes(action)) return 'invalid-action';
        if (Main.sessionMode.isLocked) return 'locked';
        if (Main.overview.visible || !this._windows().includes(global.display.focus_window)) return 'unfocused';
        const modifiers = Clutter.ModifierType.CONTROL_MASK | Clutter.ModifierType.SHIFT_MASK |
            Clutter.ModifierType.MOD1_MASK | Clutter.ModifierType.SUPER_MASK;
        if ((global.get_pointer()[2] & modifiers) !== 0) return 'modifiers-held';
        const keys = action === 'dictate' ?
            [Clutter.KEY_Control_L, Clutter.KEY_Shift_L, Clutter.KEY_d] : [Clutter.KEY_Return];
        const pressed = [];
        try {
            for (const key of keys) {
                this._keyboard.notify_keyval(0, key, Clutter.KeyState.PRESSED);
                pressed.push(key);
            }
        } finally {
            for (const key of pressed.reverse())
                this._keyboard.notify_keyval(0, key, Clutter.KeyState.RELEASED);
        }
        return 'sent';
    }
    Status() {
        return JSON.stringify({locked:Main.sessionMode.isLocked,
            windows:this._windows().map(w => ({id:w.get_id(),title:w.get_title(),
                wmclass:w.get_wm_class(),focused:global.display.focus_window === w}))});
    }
}
