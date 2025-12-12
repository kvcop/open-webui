<script lang="ts">
	import { getContext } from 'svelte';
	import { settings } from '$lib/stores';

	const i18n = getContext('i18n');

	export let saveSettings: (updated: any) => Promise<void>;

	let jiraToken = '';
	let confluenceToken = '';

	$: if ($settings) {
		jiraToken = $settings.jiraToken ?? '';
		confluenceToken = $settings.confluenceToken ?? '';
	}

	const saveHandler = async () => {
		await saveSettings({
			jiraToken,
			confluenceToken
		});
	};
</script>

<div class="flex flex-col h-full justify-between text-sm">
	<div class="space-y-3 pr-1.5 overflow-y-scroll max-h-[25rem]">
		<div class="text-sm font-medium">{$i18n.t('Integration Settings')}</div>

		<div>
			<div class=" py-0.5 flex w-full justify-between">
				<div class=" self-center text-xs font-medium">{$i18n.t('Jira Token')}</div>
			</div>

			<div class=" py-0.5 flex w-full">
				<div class=" flex-1">
					<input
						class="w-full text-sm bg-transparent border dark:border-gray-600 outline-hidden rounded-lg px-2 py-1.5 focus:border-gray-500 focus:ring-0"
						type="password"
						placeholder={$i18n.t('Enter your Jira Token')}
						bind:value={jiraToken}
					/>
				</div>
			</div>
		</div>

		<div>
			<div class=" py-0.5 flex w-full justify-between">
				<div class=" self-center text-xs font-medium">{$i18n.t('Confluence Token')}</div>
			</div>

			<div class=" py-0.5 flex w-full">
				<div class=" flex-1">
					<input
						class="w-full text-sm bg-transparent border dark:border-gray-600 outline-hidden rounded-lg px-2 py-1.5 focus:border-gray-500 focus:ring-0"
						type="password"
						placeholder={$i18n.t('Enter your Confluence Token')}
						bind:value={confluenceToken}
					/>
				</div>
			</div>
		</div>
	</div>

	<div class="flex justify-end pt-3 text-sm font-medium">
		<button
			class="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-gray-100 transition rounded-lg"
			on:click={saveHandler}
		>
			{$i18n.t('Save')}
		</button>
	</div>
</div>
