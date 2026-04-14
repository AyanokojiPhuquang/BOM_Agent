import { useNavigate } from 'react-router-dom';
import type { Conversation } from '@/types';
import { cn } from '@/utils/cn';
import { PlusIcon, ChatBubbleIcon, TrashIcon, SettingsIcon, LogoutIcon } from '@/components/icons';

interface SidebarProps {
  conversations: Conversation[];
  activeId: string | null;
  isOpen: boolean;
  userName?: string;
  userRole?: 'user' | 'admin';
  onSelectConversation: (id: string) => void;
  onNewChat: () => void;
  onDeleteConversation: (id: string) => void;
  onLogout: () => void;
  onClose: () => void;
}

export function Sidebar({
  conversations,
  activeId,
  isOpen,
  userName,
  userRole,
  onSelectConversation,
  onNewChat,
  onDeleteConversation,
  onLogout,
  onClose,
}: SidebarProps) {
  const navigate = useNavigate();
  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-20 md:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed md:static inset-y-0 left-0 z-30 w-72 bg-dark-surface border-r border-dark-border flex flex-col transition-transform duration-200',
          isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0 md:hidden'
        )}
      >
        {/* Header */}
        <div className="p-3 border-b border-dark-border">
          <button
            onClick={onNewChat}
            className="w-full flex items-center gap-2 px-3 py-2.5 rounded-xl border border-dark-border hover:bg-dark-hover transition-colors text-gray-200 text-sm"
          >
            <PlusIcon />
            New Chat
          </button>
        </div>

        {/* Conversation list */}
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {conversations.length === 0 && (
            <p className="text-gray-500 text-sm text-center py-8">No conversations yet</p>
          )}
          {conversations.map(conv => (
            <div
              key={conv.id}
              className={cn(
                'group flex items-center gap-2 px-3 py-2.5 rounded-lg cursor-pointer transition-colors text-sm',
                conv.id === activeId
                  ? 'bg-dark-hover text-white'
                  : 'text-gray-300 hover:bg-dark-hover'
              )}
              onClick={() => onSelectConversation(conv.id)}
            >
              <ChatBubbleIcon className="flex-shrink-0 text-gray-400" />
              <span className="flex-1 truncate">{conv.title}</span>
              <button
                onClick={(e) => { e.stopPropagation(); onDeleteConversation(conv.id); }}
                className="opacity-0 group-hover:opacity-100 p-1 text-gray-400 hover:text-red-400 transition-all"
              >
                <TrashIcon className="w-3.5 h-3.5" />
              </button>
            </div>
          ))}
        </div>

        {/* User section */}
        <div className="p-3 border-t border-dark-border">
          <div className="flex items-center gap-3 px-2 py-2">
            <div className="w-8 h-8 rounded-full bg-accent/20 text-accent flex items-center justify-center text-sm font-bold">
              {userName?.slice(0, 2).toUpperCase() ?? 'U'}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm text-gray-200 truncate">{userName ?? 'User'}</p>
            </div>
            <div className="flex items-center gap-1">
              {userRole === 'admin' && (
                <button
                  onClick={() => navigate('/admin')}
                  className="p-2 text-gray-400 hover:text-white rounded-lg hover:bg-dark-hover transition-colors"
                  title="Admin Settings"
                >
                  <SettingsIcon />
                </button>
              )}
              <button
                onClick={onLogout}
                className="p-2 text-gray-400 hover:text-red-400 rounded-lg hover:bg-dark-hover transition-colors"
                title="Logout"
              >
                <LogoutIcon />
              </button>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}
