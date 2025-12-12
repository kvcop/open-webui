
import { render, screen, fireEvent } from '@testing-library/svelte';
import { describe, it, expect, vi } from 'vitest';
import { writable } from 'svelte/store';
import Integration from './Integration.svelte';

// Mock stores
vi.mock('$lib/stores', () => {
    const { writable } = require('svelte/store');
    const settingsStore = writable({ jiraToken: 'old-jira', confluenceToken: 'old-conf' });
    return {
        settings: settingsStore
    };
});

describe('Integration Settings', () => {
    it('renders input fields with values from settings', () => {
        // Mock context
        const context = new Map();
        const i18nStore = writable({ t: (str: string) => str });
        context.set('i18n', i18nStore);

        render(Integration, {
            props: { saveSettings: vi.fn() },
            context: context
        });

        const jiraInput = screen.getByPlaceholderText('Enter your Jira Token') as HTMLInputElement;
        const confInput = screen.getByPlaceholderText('Enter your Confluence Token') as HTMLInputElement;

        expect(jiraInput).toBeTruthy();
        expect(confInput).toBeTruthy();

        // Check values
        expect(jiraInput.value).toBe('old-jira');
        expect(confInput.value).toBe('old-conf');
    });

    it('calls saveSettings with new values on save', async () => {
        const saveSettingsMock = vi.fn();
        const context = new Map();
        const i18nStore = writable({ t: (str: string) => str });
        context.set('i18n', i18nStore);

        render(Integration, {
            props: { saveSettings: saveSettingsMock },
            context: context
        });

        const jiraInput = screen.getByPlaceholderText('Enter your Jira Token');
        const confInput = screen.getByPlaceholderText('Enter your Confluence Token');

        await fireEvent.input(jiraInput, { target: { value: 'new-jira' } });
        await fireEvent.input(confInput, { target: { value: 'new-conf' } });

        const saveButton = screen.getByText('Save');
        await fireEvent.click(saveButton);

        expect(saveSettingsMock).toHaveBeenCalledWith({
            jiraToken: 'new-jira',
            confluenceToken: 'new-conf'
        });
    });
});
