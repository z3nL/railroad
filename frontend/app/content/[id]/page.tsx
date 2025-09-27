"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { useRouter } from "next/navigation"
import { ArrowLeft, ChevronLeft, ChevronRight, StickyNote, X } from "lucide-react"

interface ContentSlide {
  id: number
  image: string
  title: string
  description: string
}

const sampleSlides: ContentSlide[] = [
  {
    id: 1,
    image: "/mathematical-equations-and-formulas.jpg",
    title: "Introduction to Algebra",
    description:
      "Algebra is a branch of mathematics that uses symbols and letters to represent numbers and quantities in formulas and equations. It helps us solve problems by finding unknown values.",
  },
  {
    id: 2,
    image: "/geometric-shapes-and-patterns.jpg",
    title: "Basic Geometric Shapes",
    description:
      "Geometry studies shapes, sizes, and properties of figures. Basic shapes include circles, triangles, squares, and rectangles. Each shape has unique properties and formulas for calculating area and perimeter.",
  },
  {
    id: 3,
    image: "/number-line-and-integers.jpg",
    title: "Understanding Numbers",
    description:
      "Numbers are the foundation of mathematics. We use positive numbers, negative numbers, and zero to represent quantities. The number line helps us visualize and compare different values.",
  },
  {
    id: 4,
    image: "/fraction-diagrams-and-pie-charts.jpg",
    title: "Working with Fractions",
    description:
      "Fractions represent parts of a whole. They consist of a numerator (top number) and denominator (bottom number). Fractions help us describe quantities that are not whole numbers.",
  },
]

export default function ContentPage({ params }: { params: { id: string } }) {
  const [currentSlide, setCurrentSlide] = useState(0)
  const [notes, setNotes] = useState("")
  const [isNotesOpen, setIsNotesOpen] = useState(false)
  const router = useRouter()

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % sampleSlides.length)
  }

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + sampleSlides.length) % sampleSlides.length)
  }

  const currentContent = sampleSlides[currentSlide]

  return (
    <div className="min-h-screen bg-background relative">
      <div className="floating-elements">
        <div className="floating-circle w-24 h-24 top-20 left-20" style={{ animationDelay: "1s" }} />
        <div className="floating-square w-32 h-32 bottom-24 right-24" style={{ animationDelay: "3s" }} />
      </div>

      <div
        className={`fixed top-0 right-0 h-full backdrop-blur-sm border-l border-border shadow-2xl transition-transform duration-300 z-50 ${isNotesOpen ? "translate-x-0" : "translate-x-full"}`}
        style={{ width: "400px" }}
      >
        <div className="p-6 h-full flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold text-foreground flex items-center gap-2">
              <StickyNote className="w-5 h-5 text-primary" />
              Your Notes
            </h3>
            <Button variant="ghost" size="sm" onClick={() => setIsNotesOpen(false)}>
              <X className="w-4 h-4" />
            </Button>
          </div>
          <Textarea
            placeholder="Take notes about this lesson..."
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            className="flex-1 bg-input border-border resize-none"
          />
        </div>
      </div>

      <Button
        className={`fixed top-1/2 -translate-y-1/2 bg-primary text-primary-foreground hover:bg-accent shadow-lg z-40 transition-all duration-300 ${isNotesOpen ? "right-[400px]" : "right-4"}`}
        onClick={() => setIsNotesOpen(!isNotesOpen)}
        size="sm"
      >
        <StickyNote className="w-4 h-4" />
      </Button>

      <div className={`transition-all duration-300 ${isNotesOpen ? "mr-[400px]" : "mr-0"}`}>
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto">
            <div className="flex items-center gap-4 mb-8">
              <Button
                variant="outline"
                size="sm"
                onClick={() => router.push("/courses")}
                className="border-border hover:bg-secondary"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Courses
              </Button>
              <div>
                <h1 className="text-3xl font-bold text-foreground">Course Content</h1>
                <p className="text-[#4a7bb7]">
                  Slide {currentSlide + 1} of {sampleSlides.length}
                </p>
              </div>
            </div>

            {/* Image Slider */}
            <Card className="bg-card/80 backdrop-blur-sm border-border mb-8 shadow-xl">
              <CardContent className="p-0">
                <div className="relative">
                  <div className="aspect-video bg-muted rounded-t-lg overflow-hidden">
                    <img
                      src={currentContent.image || "/placeholder.svg"}
                      alt={currentContent.title}
                      className="w-full h-full object-cover"
                    />
                  </div>

                  {/* Navigation Buttons */}
                  <Button
                    variant="outline"
                    size="sm"
                    className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-white/90 hover:bg-white shadow-lg"
                    onClick={prevSlide}
                  >
                    <ChevronLeft className="w-4 h-4" />
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-white/90 hover:bg-white shadow-lg"
                    onClick={nextSlide}
                  >
                    <ChevronRight className="w-4 h-4" />
                  </Button>

                  {/* Slide Indicators */}
                  <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex gap-2">
                    {sampleSlides.map((_, index) => (
                      <button
                        key={index}
                        className={`w-3 h-3 rounded-full transition-colors shadow-sm ${
                          index === currentSlide ? "bg-primary" : "bg-white/50"
                        }`}
                        onClick={() => setCurrentSlide(index)}
                      />
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Content Description */}
            <Card className="bg-card/80 backdrop-blur-sm border-border shadow-xl">
              <CardContent className="p-6">
                <h2 className="text-2xl font-bold text-card-foreground mb-4">{currentContent.title}</h2>
                <Textarea
                  value={currentContent.description}
                  readOnly
                  className="min-h-[120px] bg-white border-border resize-none cursor-default"
                />
              </CardContent>
            </Card>

            {/* Progress Bar */}
            <div className="mt-8">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm text-muted-foreground">Progress</span>
                <span className="text-sm text-muted-foreground">
                  {Math.round(((currentSlide + 1) / sampleSlides.length) * 100)}%
                </span>
              </div>
              <div className="w-full bg-secondary rounded-full h-3 shadow-inner">
                <div
                  className="bg-primary h-3 rounded-full transition-all duration-300 shadow-sm"
                  style={{ width: `${((currentSlide + 1) / sampleSlides.length) * 100}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
