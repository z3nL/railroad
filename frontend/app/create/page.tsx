"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { useRouter } from "next/navigation"
import { ArrowLeft, Loader2, Sparkles, Plus, BookOpen } from "lucide-react"

export default function CreatePage() {
  const [title, setTitle] = useState("")
  const [topic, setTopic] = useState("")
  const [difficulty, setDifficulty] = useState("")
  const [description, setDescription] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!title || !topic || !difficulty) return

    setIsLoading(true)

    // Simulate content creation process
    setTimeout(() => {
      setIsLoading(false)
      // Generate a new course ID and redirect to the content page
      const newCourseId = Date.now().toString()
      router.push(`/content/${newCourseId}`)
    }, 2500)
  }

  return (
    <div className="min-h-screen bg-background relative">
      <div className="floating-elements">
        <div className="floating-circle w-36 h-36 top-12 right-12" style={{ animationDelay: "2s" }} />
        <div className="floating-square w-28 h-28 bottom-16 left-16" style={{ animationDelay: "4s" }} />
        <div className="floating-circle w-20 h-20 top-1/3 left-1/4" style={{ animationDelay: "6s" }} />
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <div className="flex items-center gap-4 mb-8">
            <Button
              variant="outline"
              size="sm"
              onClick={() => router.push("/courses")}
              className="border-border hover:bg-secondary"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Lessons
            </Button>
          </div>

          <div className="mb-6">
            <h1 className="text-3xl font-bold text-foreground flex items-center gap-2">
              <BookOpen className="w-8 h-8 text-primary" />
              Create New Content
            </h1>
            <p className="text-[#4a7bb7]">Design educational content for students</p>
          </div>

          <Card className="bg-card/80 backdrop-blur-sm border-border shadow-xl">
            <CardHeader>
              <CardTitle className="text-2xl flex items-center gap-2">
                <Sparkles className="w-6 h-6 text-primary" />
                Lesson Details
              </CardTitle>
              <CardDescription>Fill in the information below to create new educational content</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                  <label htmlFor="title" className="text-sm font-medium">
                    Lesson Title
                  </label>
                  <Input
                    id="title"
                    placeholder="Enter lesson title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
                    className="bg-input border-border placeholder:text-[#7ba3d3]"
                  />
                </div>

                <div className="space-y-2">
                  <label htmlFor="topic" className="text-sm font-medium">
                    Topic/Subject
                  </label>
                  <Select value={topic} onValueChange={setTopic} required>
                    <SelectTrigger className="bg-input border-border [&>svg]:text-[#7ba3d3] relative">
                      <SelectValue placeholder="Select a topic ▼" className="placeholder:text-[#7ba3d3]" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Math">Mathematics</SelectItem>
                      <SelectItem value="Science">Science</SelectItem>
                      <SelectItem value="History">History</SelectItem>
                      <SelectItem value="Language">Language Arts</SelectItem>
                      <SelectItem value="Art">Art & Design</SelectItem>
                      <SelectItem value="Geography">Geography</SelectItem>
                      <SelectItem value="Music">Music</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <label htmlFor="difficulty" className="text-sm font-medium">
                    Difficulty Level
                  </label>
                  <Select value={difficulty} onValueChange={setDifficulty} required>
                    <SelectTrigger className="bg-input border-border [&>svg]:text-[#7ba3d3] relative">
                      <SelectValue placeholder="Select difficulty level ▼" className="placeholder:text-[#7ba3d3]" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Elementary">Elementary</SelectItem>
                      <SelectItem value="Secondary School">Secondary School</SelectItem>
                      <SelectItem value="College">College</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <label htmlFor="description" className="text-sm font-medium">
                    Description
                  </label>
                  <Textarea
                    id="description"
                    placeholder="Describe what students will learn in this lesson"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={4}
                    className="bg-input border-border placeholder:text-[#7ba3d3]"
                  />
                </div>

                <Button
                  type="submit"
                  className="w-full bg-primary text-primary-foreground hover:bg-accent shadow-xl transform hover:scale-[1.02] transition-all duration-300 py-8 text-xl font-bold rounded-xl border-2 border-primary/20"
                  disabled={isLoading || !title || !topic || !difficulty}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-6 h-6 mr-3 animate-spin" />
                      Creating Your Lesson...
                    </>
                  ) : (
                    <>
                      <Plus className="w-6 h-6 mr-3" />
                      Create Lesson
                    </>
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
