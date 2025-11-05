export interface AvatarAppearance {
  gender: 'male' | 'female' | 'neutral';
  style: 'professional' | 'casual' | 'creative' | 'fun';
  age: 'young' | 'adult' | 'mature';
}

export interface AvatarAnimations {
  idle: boolean;
  talking: boolean;
  listening: boolean;
  thinking: boolean;
  gestures: boolean;
}

export interface Avatar {
  provider: 'simli' | 'tavus' | 'hedra' | 'bithuman' | 'anam' | 'bey';
  avatarId: string;
  appearance: AvatarAppearance;
  animations: AvatarAnimations;
}

export interface Personality {
  traits: string[];
  tone: 'warm' | 'professional' | 'playful' | 'serious';
  energy: 'low' | 'medium' | 'high';
  humor: 'none' | 'light' | 'moderate' | 'heavy';
  formality: 'formal' | 'casual' | 'mixed';
}

export interface Voice {
  provider: 'openai' | 'elevenlabs' | 'deepgram';
  voiceId: string;
  speed: number;
  pitch: number;
}

export interface ToolParameter {
  type: string;
  description: string;
  required?: boolean;
}

export interface Tool {
  name: string;
  description: string;
  parameters: Record<string, ToolParameter>;
  enabled: boolean;
}

export interface Capabilities {
  interruption: boolean;
  memory: boolean;
  multimodal: boolean;
  multilingual: boolean;
}

export interface AgentConfig {
  name: string;
  avatar: Avatar;
  personality: Personality;
  voice: Voice;
  tools: Tool[];
  capabilities: Capabilities;
}

export interface AvatarProvider {
  id: string;
  name: string;
  description: string;
  features: string[];
  pricing: 'free' | 'paid' | 'freemium';
  previewUrl?: string;
}

export interface Template {
  id: string;
  name: string;
  description: string;
  personality: Partial<Personality>;
  tools: string[];
  preview?: string;
}
