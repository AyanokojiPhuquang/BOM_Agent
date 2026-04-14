import { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { cn } from '@/utils/cn';
import { BackArrowIcon, UsersIcon, FolderOutlineIcon, CollapseIcon } from '@/components/icons';
import { UserManagementContent } from '@/pages/UserManagementPage';
import { FileManagementContent } from '@/pages/FileManagementPage';

const TABS = [
  { key: 'users', label: 'Users', icon: <UsersIcon /> },
  { key: 'files', label: 'Files', icon: <FolderOutlineIcon /> },
] as const;

type TabKey = (typeof TABS)[number]['key'];

export function AdminSettingsPage() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const initialTab = (searchParams.get('tab') as TabKey) || 'users';
  const [activeTab, setActiveTab] = useState<TabKey>(initialTab);
  const [collapsed, setCollapsed] = useState(false);

  const handleTabChange = (tab: TabKey) => {
    setActiveTab(tab);
    setSearchParams({ tab });
  };

  return (
    <div className="h-screen bg-dark-bg flex flex-col">
      {/* Header */}
      <header className="flex items-center gap-4 px-6 py-4 border-b border-dark-border bg-dark-surface">
        <button
          onClick={() => navigate('/chat')}
          className="p-2 text-gray-400 hover:text-white rounded-lg hover:bg-dark-hover transition-colors"
        >
          <BackArrowIcon />
        </button>
        <h1 className="text-xl font-semibold text-white">Admin Settings</h1>
      </header>

      {/* Sidebar + Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Collapsible sidebar nav */}
        <nav className={cn(
          'flex-shrink-0 border-r border-dark-border bg-dark-surface flex flex-col transition-all duration-200',
          collapsed ? 'w-14' : 'w-48'
        )}>
          <div className="p-2 space-y-1 flex-1">
            {TABS.map(tab => (
              <button
                key={tab.key}
                onClick={() => handleTabChange(tab.key)}
                title={collapsed ? tab.label : undefined}
                className={cn(
                  'w-full flex items-center gap-2 rounded-lg text-sm font-medium transition-colors',
                  collapsed ? 'justify-center px-2 py-2' : 'px-3 py-2',
                  activeTab === tab.key
                    ? 'bg-accent/15 text-accent'
                    : 'text-gray-400 hover:text-white hover:bg-dark-hover'
                )}
              >
                {tab.icon}
                {!collapsed && <span>{tab.label}</span>}
              </button>
            ))}
          </div>
          <button
            onClick={() => setCollapsed(c => !c)}
            className="p-3 border-t border-dark-border text-gray-400 hover:text-white transition-colors flex justify-center"
            title={collapsed ? 'Expand' : 'Collapse'}
          >
            <CollapseIcon className={cn('transition-transform', collapsed && 'rotate-180')} />
          </button>
        </nav>

        {/* Content */}
        <div className="flex-1 overflow-auto">
          {activeTab === 'users' && <UserManagementContent />}
          {activeTab === 'files' && <FileManagementContent />}
        </div>
      </div>
    </div>
  );
}
