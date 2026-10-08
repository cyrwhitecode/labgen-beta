export interface messageType {
	sender: 'user' | 'assistant';
	content: string;
}

export interface DateType {
	date: string;
	heure: string;
}

export interface ContextType {
	id: string;
	title: string;
	subject: string;
	object: string;
	date: DateType;
	messages: messageType[];
} 


