import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const viewport: Viewport = {
  themeColor: "#2563eb",
}

export const metadata: Metadata = {
  title: "CRC MedQA - 结直肠癌专业医学问答助手",
  description: "基于CSCO、NCCN、ESMO等权威指南的结直肠癌医学知识库，支持智能问答、知识浏览和离线下载。",
  keywords: ["结直肠癌", "结肠癌", "直肠癌", "医学知识库", "CSCO指南", "NCCN指南", "AI问答"],
  authors: [{ name: "汪晓东" }],
  openGraph: {
    title: "CRC MedQA - 结直肠癌专业医学问答助手",
    description: "557+条权威医学知识，7大知识领域，助您了解结直肠癌",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="zh-CN"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
