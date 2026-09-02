---
title: vibe coding 類似 Glass2k 功能調整視窗透明度
date: 2026-01-05 18:49:25
tags:
---
&nbsp;
<!-- more -->

以前學 css 的時候老師會用一個工具 Glass2k 他應該是 vb6 做的
可是防毒好像都會叫, 某次不明帳號登入信箱後懷疑跟他有關也就沒再用

現在 vibe coding 當道想說來還原看看, 沒想到也是能搞定 LOL

```
using System;
using System.Drawing;
using System.Runtime.InteropServices;
using System.Text;
using System.Windows.Forms;

namespace ActualTransparent
{
    public partial class TransparentForm : Form
    {
        private NotifyIcon trayIcon;
        private byte alpha = 160;
        private IntPtr targetHwnd = IntPtr.Zero;
        private bool isTransparent = false;

        // 初始熱鍵
        private Keys hotKeyMain = Keys.T;
        private HotKeyManager.Modifiers hotKeyModifier = HotKeyManager.Modifiers.Control | HotKeyManager.Modifiers.Alt;

        // 控制元件
        private TrackBar tbAlpha;
        private ComboBox modifierBox;
        private ComboBox keyBox;
        private Button btnSetHotKey;
        private Label lblLow;
        private Label lblHigh;

        public TransparentForm()
        {
            // 設定窗體屬性
            this.Text = "透明人間";
            this.Size = new Size(400, 300);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.TopMost = true;
            this.FormBorderStyle = FormBorderStyle.FixedToolWindow;

            // 系統托盤
            trayIcon = new NotifyIcon
            {
                Icon = SystemIcons.Application,
                Visible = true,
                Text = "透明人間"
            };

            var contextMenu = new ContextMenuStrip();
            var exitItem = new ToolStripMenuItem("Exit");
            exitItem.Click += (s, e) =>
            {
                trayIcon.Visible = false;
                Application.Exit();
            };
            contextMenu.Items.Add(exitItem);
            trayIcon.ContextMenuStrip = contextMenu;

            // 左鍵點擊顯示/隱藏窗體
            trayIcon.MouseClick += (s, e) =>
            {
                if (e.Button == MouseButtons.Left)
                {
                    if (!this.Visible)
                    {
                        this.Show();
                        this.WindowState = FormWindowState.Normal;
                        this.BringToFront();
                    }
                    else
                    {
                        this.Hide();
                    }
                }
            };

            // 建立控制元件
            InitializeControls();

            // 註冊全局熱鍵
            HotKeyManager.RegisterHotKey(hotKeyMain, hotKeyModifier);
            Application.AddMessageFilter(new HotKeyMessageFilter(OnHotKeyPressed));
        }

        protected override void OnFormClosing(FormClosingEventArgs e)
        {
            if (e.CloseReason == CloseReason.UserClosing)
            {
                e.Cancel = true;    // 取消關閉
                this.Hide();        // 隱藏到托盤
            }
            else
            {
                trayIcon.Visible = false;
                HotKeyManager.UnregisterAllHotKeys();
                base.OnFormClosing(e);
            }
        }

        private void InitializeControls()
        {
            // TrackBar
            tbAlpha = new TrackBar
            {
                Minimum = 50,
                Maximum = 255,
                Value = alpha,
                Orientation = Orientation.Vertical,
                TickFrequency = 10,
                Height = 180,
                Left = 50,
                Top = 40
            };
            tbAlpha.Scroll += (s, e) => alpha = (byte)tbAlpha.Value;
            this.Controls.Add(tbAlpha);

            // Low / High 標籤
            lblLow = new Label
            {
                Text = "低",
                Left = tbAlpha.Left - 40,
                Top = tbAlpha.Top + tbAlpha.Height - 15,
                Width = 40,
                TextAlign = ContentAlignment.MiddleRight
            };
            lblHigh = new Label
            {
                Text = "高",
                Left = tbAlpha.Left - 40,
                Top = tbAlpha.Top - 5,
                Width = 40,
                TextAlign = ContentAlignment.MiddleRight
            };
            this.Controls.Add(lblLow);
            this.Controls.Add(lblHigh);

            // Modifier ComboBox
            modifierBox = new ComboBox { Left = 150, Top = 40, Width = 200 };
            modifierBox.Items.AddRange(new string[] { "Control", "Alt", "Shift", "Win", "Ctrl+Alt", "Ctrl+Shift", "Alt+Shift" });
            modifierBox.SelectedItem = "Ctrl+Alt";
            this.Controls.Add(modifierBox);

            // Key ComboBox 限制 0~9 與 A~Z
            keyBox = new ComboBox { Left = 150, Top = 80, Width = 200 };
            for (char c = 'A'; c <= 'Z'; c++) keyBox.Items.Add((Keys)Enum.Parse(typeof(Keys), c.ToString()));
            keyBox.SelectedItem = Keys.T;
            this.Controls.Add(keyBox);

            // 設定熱鍵按鈕
            btnSetHotKey = new Button
            {
                Text = "設定熱鍵",
                Left = 150,
                Top = 120,
                Width = 200,
                Height = 40,
                Font = new Font("Segoe UI", 10, FontStyle.Bold)
            };
            btnSetHotKey.Click += (s, e) =>
            {
                HotKeyManager.UnregisterAllHotKeys();
                hotKeyMain = (Keys)keyBox.SelectedItem;
                hotKeyModifier = ParseModifiers(modifierBox.SelectedItem.ToString());
                HotKeyManager.RegisterHotKey(hotKeyMain, hotKeyModifier);
            };
            this.Controls.Add(btnSetHotKey);
        }

        private HotKeyManager.Modifiers ParseModifiers(string text)
        {
            HotKeyManager.Modifiers mods = 0;
            if (text.Contains("Control") || text.Contains("Ctrl")) mods |= HotKeyManager.Modifiers.Control;
            if (text.Contains("Alt")) mods |= HotKeyManager.Modifiers.Alt;
            if (text.Contains("Shift")) mods |= HotKeyManager.Modifiers.Shift;
            if (text.Contains("Win")) mods |= HotKeyManager.Modifiers.Win;
            return mods;
        }

        private void OnHotKeyPressed()
        {
            Win32.GetCursorPos(out Point pt);
            IntPtr hwnd = Win32.WindowFromPoint(pt);

            if (hwnd == IntPtr.Zero || hwnd == this.Handle || IsSystemWindow(hwnd))
                return;

            if (!isTransparent)
            {
                SetAlphaRecursive(hwnd, alpha);
                targetHwnd = hwnd;
                isTransparent = true;
            }
            else
            {
                if (targetHwnd != IntPtr.Zero)
                    SetAlphaRecursive(targetHwnd, 255);
                isTransparent = false;
            }
        }

        // 遞迴設透明
        private void SetAlphaRecursive(IntPtr hwnd, byte a)
        {
            SetAlpha(hwnd, a);
            IntPtr child = Win32.GetWindow(hwnd, Win32.GW_CHILD);
            while (child != IntPtr.Zero)
            {
                SetAlphaRecursive(child, a);
                child = Win32.GetWindow(child, Win32.GW_HWNDNEXT);
            }
        }

        private void SetAlpha(IntPtr hwnd, byte a)
        {
            int style = Win32.GetWindowLong(hwnd, Win32.GWL_EXSTYLE);
            if ((style & Win32.WS_EX_LAYERED) == 0)
                Win32.SetWindowLong(hwnd, Win32.GWL_EXSTYLE, style | Win32.WS_EX_LAYERED);

            Win32.SetLayeredWindowAttributes(hwnd, 0, a, Win32.LWA_ALPHA);
        }

        private bool IsSystemWindow(IntPtr hwnd)
        {
            if (hwnd == IntPtr.Zero) return true;

            IntPtr root = Win32.GetAncestor(hwnd, 3); // GA_ROOTOWNER
            string className = GetClassName(root);
            if (string.IsNullOrEmpty(className)) return true;

            string[] systemClasses = { "Shell_TrayWnd", "DV2ControlHost", "Windows.UI.Core.CoreWindow" };
            foreach (var sys in systemClasses)
                if (className == sys) return true;

            IntPtr taskbar = Win32.FindWindow("Shell_TrayWnd", null);
            if (taskbar != IntPtr.Zero && Win32.IsChild(taskbar, hwnd)) return true;

            if (root == this.Handle) return true;

            return false;
        }

        private string GetClassName(IntPtr hwnd)
        {
            StringBuilder sb = new StringBuilder(256);
            int ret = Win32.GetClassName(hwnd, sb, sb.Capacity);
            if (ret > 0)
                return sb.ToString();
            return "";
        }
    }

    public class HotKeyMessageFilter : IMessageFilter
    {
        private const int WM_HOTKEY = 0x0312;
        private Action callback;
        public HotKeyMessageFilter(Action callback) { this.callback = callback; }
        public bool PreFilterMessage(ref Message m)
        {
            if (m.Msg == WM_HOTKEY)
            {
                callback?.Invoke();
                return true;
            }
            return false;
        }
    }

    public static class HotKeyManager
    {
        public enum Modifiers : uint { Alt = 1, Control = 2, Shift = 4, Win = 8 }
        private static int idCounter = 0;

        [DllImport("user32.dll")]
        private static extern bool RegisterHotKey(IntPtr hWnd, int id, uint fsModifiers, uint vk);

        [DllImport("user32.dll")]
        private static extern bool UnregisterHotKey(IntPtr hWnd, int id);

        public static void RegisterHotKey(Keys key, Modifiers mods)
        {
            idCounter++;
            RegisterHotKey(IntPtr.Zero, idCounter, (uint)mods, (uint)key);
        }

        public static void UnregisterAllHotKeys()
        {
            for (int i = 1; i <= idCounter; i++)
                UnregisterHotKey(IntPtr.Zero, i);
            idCounter = 0;
        }
    }

    public static class Win32
    {
        public const int GWL_EXSTYLE = -20;
        public const int WS_EX_LAYERED = 0x80000;
        public const int LWA_ALPHA = 0x2;
        public const uint GA_ROOT = 2;
        public const uint GA_ROOTOWNER = 3;
        public const uint GW_CHILD = 5;
        public const uint GW_HWNDNEXT = 2;

        [DllImport("user32.dll")]
        public static extern IntPtr WindowFromPoint(Point p);

        [DllImport("user32.dll")]
        public static extern bool GetCursorPos(out Point lpPoint);

        [DllImport("user32.dll")]
        public static extern int GetWindowLong(IntPtr hWnd, int nIndex);

        [DllImport("user32.dll")]
        public static extern int SetWindowLong(IntPtr hWnd, int nIndex, int dwNewLong);

        [DllImport("user32.dll")]
        public static extern bool SetLayeredWindowAttributes(IntPtr hwnd, uint crKey, byte bAlpha, uint dwFlags);

        [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        public static extern int GetClassName(IntPtr hWnd, StringBuilder lpClassName, int nMaxCount);

        [DllImport("user32.dll")]
        public static extern IntPtr GetAncestor(IntPtr hwnd, uint gaFlags);

        [DllImport("user32.dll")]
        public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);

        [DllImport("user32.dll")]
        public static extern bool IsChild(IntPtr hWndParent, IntPtr hWnd);

        [DllImport("user32.dll")]
        public static extern IntPtr GetParent(IntPtr hWnd);

        [DllImport("user32.dll")]
        public static extern IntPtr GetWindow(IntPtr hWnd, uint uCmd);
    }
}
```
