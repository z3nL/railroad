"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { useRouter } from "next/navigation"
import { ArrowLeft, Plus } from "lucide-react"

interface Lesson {
  id: string
  title: string
  subject: string
  difficulty: "Elementary" | "Secondary School" | "College"
  description: string
}

const lessons: Lesson[] = [
  {
    id: "1",
    title: "Introduction to Mathematics",
    subject: "Math",
    difficulty: "Elementary",
    description: "Learn basic math concepts through visual examples",
  },
  {
    id: "2",
    title: "World History Timeline",
    subject: "History",
    difficulty: "Secondary School",
    description: "Explore major historical events with interactive timelines",
  },
  {
    id: "3",
    title: "Biology Fundamentals",
    subject: "Science",
    difficulty: "College",
    description: "Advanced biological concepts with detailed illustrations",
  },
  {
    id: "4",
    title: "Creative Writing Workshop",
    subject: "Language",
    difficulty: "Secondary School",
    description: "Develop writing skills through guided exercises",
  },
  {
    id: "5",
    title: "Art History Masterpieces",
    subject: "Art",
    difficulty: "College",
    description: "Study famous artworks and their historical context",
  },
]

const getSubjectColor = (subject: string) => {
  const colors = {
    Math: "bg-primary/20 text-primary border-primary/30",
    Science: "bg-accent/20 text-accent border-accent/30",
    History: "bg-secondary/20 text-secondary border-secondary/30",
    Language: "bg-muted/20 text-muted border-muted/30",
    Art: "bg-primary/30 text-primary border-primary/40",
  }
  return colors[subject as keyof typeof colors] || "bg-muted/20 text-muted border-muted/30"
}

const getDifficultyColor = (difficulty: string) => {
  const colors = {
    Elementary: "bg-accent/10 text-accent border-accent/20",
    "Secondary School": "bg-secondary/10 text-secondary border-secondary/20",
    College: "bg-primary/10 text-primary border-primary/20",
  }
  return colors[difficulty as keyof typeof colors] || "bg-muted/10 text-muted border-muted/20"
}

export default function LessonsPage() {
  const router = useRouter()

  return (
    <div className="min-h-screen bg-background relative">
      <div className="floating-elements">
        <div className="floating-circle w-28 h-28 top-16 right-16" style={{ animationDelay: "1s" }} />
        <div className="floating-square w-32 h-32 bottom-20 left-20" style={{ animationDelay: "3s" }} />
        <div className="floating-circle w-24 h-24 top-1/2 left-10" style={{ animationDelay: "5s" }} />
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <Button
              variant="outline"
              size="sm"
              onClick={() => router.push("/")}
              className="border-border hover:bg-secondary"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back
            </Button>
            <div>
              <h1 className="text-3xl font-bold text-foreground">Available Lessons</h1>
              <p className="text-[#4a7bb7]">Choose a lesson to start learning</p>
            </div>
          </div>
          <Button
            onClick={() => router.push("/create")}
            className="bg-primary text-primary-foreground hover:bg-accent shadow-lg"
          >
            <Plus className="w-4 h-4 mr-2" />
            Create New Lesson
          </Button>
        </div>

        <div className="space-y-4">
          <div className="grid grid-cols-12 gap-4 px-6 py-3 bg-secondary/10 rounded-lg border border-border/30">
            <div className="col-span-4 font-semibold text-foreground">Lesson Title</div>
            <div className="col-span-2 font-semibold text-foreground">Subject</div>
            <div className="col-span-2 font-semibold text-foreground">Difficulty</div>
            <div className="col-span-3 font-semibold text-foreground">Description</div>
            <div className="col-span-1 font-semibold text-foreground">Action</div>
          </div>

          {lessons.map((lesson) => (
            <Card
              key={lesson.id}
              className="bg-card/80 backdrop-blur-sm border-border hover:shadow-lg transition-all duration-200 cursor-pointer hover:bg-card"
              onClick={() => router.push(`/content/${lesson.id}`)}
            >
              <CardContent className="p-0">
                <div className="grid grid-cols-12 gap-4 px-6 py-4 items-center">
                  <div className="col-span-4">
                    <h3 className="text-lg font-semibold text-card-foreground mb-1">{lesson.title}</h3>
                  </div>
                  <div className="col-span-2">
                    <Badge className={getSubjectColor(lesson.subject)}>{lesson.subject}</Badge>
                  </div>
                  <div className="col-span-2">
                    <Badge variant="outline" className={getDifficultyColor(lesson.difficulty)}>
                      {lesson.difficulty}
                    </Badge>
                  </div>
                  <div className="col-span-3">
                    <p className="text-sm text-[#4a7bb7] line-clamp-2">{lesson.description}</p>
                  </div>
                  <div className="col-span-1">
                    <Button
                      variant="outline"
                      size="sm"
                      className="border-border hover:bg-primary hover:text-primary-foreground transition-colors bg-transparent"
                      onClick={(e) => {
                        e.stopPropagation()
                        router.push(`/content/${lesson.id}`)
                      }}
                    >
                      Start
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}
