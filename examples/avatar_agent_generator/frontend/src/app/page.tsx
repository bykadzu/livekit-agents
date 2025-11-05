'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Download, Play, Copy, Check } from 'lucide-react';
import AvatarSelector from '@/components/AvatarSelector';
import PersonalityBuilder from '@/components/PersonalityBuilder';
import ToolsSelector from '@/components/ToolsSelector';
import AnimationConfig from '@/components/AnimationConfig';
import CodePreview from '@/components/CodePreview';
import PreviewPanel from '@/components/PreviewPanel';
import { generateAgentCode } from '@/lib/generator';
import { AgentConfig } from '@/types';
import toast from 'react-hot-toast';

export default function Home() {
  const [step, setStep] = useState(1);
  const [config, setConfig] = useState<AgentConfig>({
    name: 'MyAgent',
    avatar: {
      provider: 'simli',
      avatarId: '',
      appearance: {
        gender: 'neutral',
        style: 'professional',
        age: 'adult',
      },
      animations: {
        idle: true,
        talking: true,
        listening: true,
        thinking: true,
        gestures: true,
      },
    },
    personality: {
      traits: ['friendly', 'professional', 'helpful'],
      tone: 'warm',
      energy: 'medium',
      humor: 'light',
      formality: 'casual',
    },
    voice: {
      provider: 'openai',
      voiceId: 'shimmer',
      speed: 1.0,
      pitch: 1.0,
    },
    tools: [],
    capabilities: {
      interruption: true,
      memory: true,
      multimodal: false,
      multilingual: false,
    },
  });

  const [generatedCode, setGeneratedCode] = useState('');
  const [copied, setCopied] = useState(false);

  const updateConfig = (updates: Partial<AgentConfig>) => {
    setConfig((prev) => ({ ...prev, ...updates }));
  };

  const handleGenerate = async () => {
    try {
      const code = await generateAgentCode(config);
      setGeneratedCode(code);
      toast.success('Agent code generated successfully!');
      setStep(5);
    } catch (error) {
      toast.error('Failed to generate agent code');
      console.error(error);
    }
  };

  const handleCopy = async () => {
    await navigator.clipboard.writeText(generatedCode);
    setCopied(true);
    toast.success('Code copied to clipboard!');
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([generatedCode], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${config.name.toLowerCase().replace(/\s+/g, '_')}_agent.py`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast.success('Agent code downloaded!');
  };

  const steps = [
    { id: 1, title: 'Avatar', component: AvatarSelector },
    { id: 2, title: 'Personality', component: PersonalityBuilder },
    { id: 3, title: 'Tools', component: ToolsSelector },
    { id: 4, title: 'Animations', component: AnimationConfig },
    { id: 5, title: 'Generate', component: CodePreview },
  ];

  const CurrentStepComponent = steps[step - 1].component;

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
      {/* Header */}
      <header className="border-b border-white/10 bg-black/20 backdrop-blur-lg">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Sparkles className="w-8 h-8 text-purple-400" />
              <h1 className="text-2xl font-bold text-white">
                AI Avatar Agent Generator
              </h1>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-purple-300">
                Powered by LiveKit Agents
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Progress Steps */}
      <div className="border-b border-white/10 bg-black/10 backdrop-blur-lg">
        <div className="container mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            {steps.map((s, idx) => (
              <div key={s.id} className="flex items-center flex-1">
                <button
                  onClick={() => setStep(s.id)}
                  className={`flex items-center gap-2 ${
                    step === s.id
                      ? 'text-purple-400'
                      : step > s.id
                      ? 'text-green-400'
                      : 'text-gray-500'
                  }`}
                >
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center ${
                      step === s.id
                        ? 'bg-purple-500 text-white'
                        : step > s.id
                        ? 'bg-green-500 text-white'
                        : 'bg-gray-700 text-gray-400'
                    }`}
                  >
                    {step > s.id ? '✓' : s.id}
                  </div>
                  <span className="font-medium">{s.title}</span>
                </button>
                {idx < steps.length - 1 && (
                  <div className="flex-1 h-0.5 bg-gray-700 mx-4" />
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Panel - Configuration */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20"
            >
              <CurrentStepComponent config={config} updateConfig={updateConfig} />

              {/* Navigation Buttons */}
              <div className="flex justify-between mt-8 pt-6 border-t border-white/10">
                <button
                  onClick={() => setStep(Math.max(1, step - 1))}
                  disabled={step === 1}
                  className="px-6 py-2 bg-white/10 hover:bg-white/20 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg text-white font-medium transition-colors"
                >
                  Previous
                </button>
                {step < 5 ? (
                  <button
                    onClick={() => setStep(Math.min(5, step + 1))}
                    className="px-6 py-2 bg-purple-500 hover:bg-purple-600 rounded-lg text-white font-medium transition-colors"
                  >
                    Next
                  </button>
                ) : (
                  <div className="flex gap-3">
                    <button
                      onClick={handleCopy}
                      className="px-6 py-2 bg-blue-500 hover:bg-blue-600 rounded-lg text-white font-medium transition-colors flex items-center gap-2"
                    >
                      {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                      {copied ? 'Copied!' : 'Copy'}
                    </button>
                    <button
                      onClick={handleDownload}
                      className="px-6 py-2 bg-green-500 hover:bg-green-600 rounded-lg text-white font-medium transition-colors flex items-center gap-2"
                    >
                      <Download className="w-4 h-4" />
                      Download
                    </button>
                  </div>
                )}
              </div>

              {step < 5 && (
                <button
                  onClick={handleGenerate}
                  className="w-full mt-4 px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 rounded-lg text-white font-bold text-lg transition-all transform hover:scale-105 flex items-center justify-center gap-2"
                >
                  <Sparkles className="w-5 h-5" />
                  Generate Agent Now
                </button>
              )}
            </motion.div>
          </div>

          {/* Right Panel - Preview */}
          <div className="lg:col-span-1">
            <PreviewPanel config={config} generatedCode={generatedCode} />
          </div>
        </div>
      </div>
    </div>
  );
}
