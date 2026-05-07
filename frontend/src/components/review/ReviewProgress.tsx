"use client"; 
import { useEffect, useState } from "react"; 

const STEPS = [ 
  { id: 1, label: "Fetching repository files",        duration: 2000 }, 
  { id: 2, label: "Selecting key files for review",   duration: 1000 }, 
  { id: 3, label: "Running Security agent",           duration: 3000 }, 
  { id: 4, label: "Running Code Quality agent",       duration: 3000 }, 
  { id: 5, label: "Running Architecture agent",       duration: 3000 }, 
  { id: 6, label: "Aggregating and scoring results",  duration: 1000 }, 
  { id: 7, label: "Saving review to database",        duration: 500  }, 
]; 

interface ReviewProgressProps { 
  isLoading: boolean; 
  projectName: string; 
} 

export function ReviewProgress({ isLoading, projectName }: ReviewProgressProps) { 
  const [currentStep, setCurrentStep] = useState(0); 
  const [completedSteps, setCompletedSteps] = useState<number[]>([]); 

  useEffect(() => { 
    if (!isLoading) return; 
    setCurrentStep(0); 
    setCompletedSteps([]); 

    let stepIndex = 0; 
    const advance = () => { 
      if (stepIndex >= STEPS.length) return; 
      setCurrentStep(stepIndex + 1); 
      const timer = setTimeout(() => { 
        setCompletedSteps(prev => [...prev, stepIndex + 1]); 
        stepIndex++; 
        advance(); 
      }, STEPS[stepIndex].duration); 
      return timer; 
    }; 

    const t = advance(); 
    return () => {
      if (t) clearTimeout(t as any);
    }; 
  }, [isLoading]); 

  if (!isLoading) return null; 

  const progress = Math.round((completedSteps.length / STEPS.length) * 100); 

  return ( 
    <div style={{ 
      background: "var(--color-background-primary)", 
      border: "0.5px solid var(--color-border-tertiary)", 
      borderRadius: "12px", 
      padding: "24px", 
      marginTop: "16px" 
    }}> 
      <div style={{ marginBottom: "16px" }}> 
        <div style={{ fontSize: "13px", fontWeight: 500, marginBottom: "4px" }}> 
          Analysing {projectName}... 
        </div> 
        <div style={{ fontSize: "11px", color: "var(--color-text-tertiary)" }}> 
          {progress}% complete 
        </div> 
      </div> 

      {/* Progress bar */} 
      <div style={{ 
        height: "4px", 
        background: "var(--color-border-tertiary)", 
        borderRadius: "2px", 
        overflow: "hidden", 
        marginBottom: "20px" 
      }}> 
        <div style={{ 
          height: "100%", 
          width: `${progress}%`, 
          background: "#378ADD", 
          borderRadius: "2px", 
          transition: "width 0.5s ease" 
        }} /> 
      </div> 

      {/* Steps */} 
      <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}> 
        {STEPS.map(step => { 
          const done = completedSteps.includes(step.id); 
          const active = currentStep === step.id; 
          return ( 
            <div key={step.id} style={{ 
              display: "flex", alignItems: "center", gap: "10px", 
              opacity: done || active ? 1 : 0.4 
            }}> 
              <div style={{ 
                width: "20px", height: "20px", borderRadius: "50%", 
                background: done ? "#22c55e" : active ? "#378ADD" : "var(--color-border-secondary)", 
                display: "flex", alignItems: "center", justifyContent: "center", 
                flexShrink: 0, transition: "background 0.3s" 
              }}> 
                {done ? ( 
                  <svg width="10" height="10" viewBox="0 0 10 10" fill="none"> 
                    <path d="M2 5l2.5 2.5L8 3" stroke="white" strokeWidth="1.5" strokeLinecap="round"/> 
                  </svg> 
                ) : active ? ( 
                  <div style={{ 
                    width: "6px", height: "6px", borderRadius: "50%", 
                    background: "white", animation: "pulse 1s infinite" 
                  }} /> 
                ) : null} 
              </div> 
              <span style={{ 
                fontSize: "12px", 
                color: active ? "var(--color-text-primary)" : "var(--color-text-secondary)", 
                fontWeight: active ? 500 : 400 
              }}> 
                {step.label} 
                {active && <span style={{ marginLeft: "6px", color: "#378ADD" }}>...</span>} 
              </span> 
            </div> 
          ); 
        })} 
      </div> 

      <style>{` 
        @keyframes pulse { 
          0%, 100% { opacity: 1; } 
          50% { opacity: 0.3; } 
        } 
      `}</style> 
    </div> 
  ); 
} 
