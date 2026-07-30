import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import { Providers } from "./providers"
import { NavBar } from "@/components/layout/NavBar"
import { MainContent } from "@/components/layout/MainContent"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "GobTools",
  description: "Plateforme open source d'outils propulsés par LLM",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>
          <NavBar />
          <MainContent>{children}</MainContent>
        </Providers>
      </body>
    </html>
  )
}
