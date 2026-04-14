import { cn } from '@/utils/cn';

interface AvatarProps {
  name: string;
  isBot?: boolean;
  className?: string;
}

export function Avatar({ name, isBot = false, className }: AvatarProps) {
  const initials = isBot ? 'AI' : name.slice(0, 2).toUpperCase();

  return (
    <div
      className={cn(
        'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold',
        isBot ? 'bg-accent text-white' : 'bg-dark-hover text-gray-300',
        className
      )}
    >
      {initials}
    </div>
  );
}
