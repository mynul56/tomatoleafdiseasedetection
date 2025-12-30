import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/chat_message.dart';
import '../services/groq_service.dart';
import '../l10n/app_localizations.dart';
import '../providers/language_provider.dart';

class AiAssistantScreen extends StatefulWidget {
  const AiAssistantScreen({super.key});

  @override
  State<AiAssistantScreen> createState() => _AiAssistantScreenState();
}

class _AiAssistantScreenState extends State<AiAssistantScreen> {
  final List<ChatMessage> _messages = [];
  final TextEditingController _textController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final GroqService _groqService = GroqService();

  bool _isLoading = false;

  void _addWelcomeMessage() {
    final languageProvider = Provider.of<LanguageProvider>(
      context,
      listen: false,
    );

    // Update services language
    _groqService.setLanguage(languageProvider.locale.languageCode);

    final l10n = AppLocalizations.of(context);
    setState(() {
      _messages.add(
        ChatMessage(
          text: '${l10n.welcomeAI}\n\n${l10n.demoMode}\n\n${l10n.askQuestion}',
          isUser: false,
        ),
      );
    });
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (_messages.isEmpty) {
      _addWelcomeMessage();
    }
  }

  Future<void> _sendMessage(String text) async {
    if (text.trim().isEmpty) return;

    setState(() {
      _messages.add(ChatMessage(text: text, isUser: true));
      _isLoading = true;
    });

    _textController.clear();
    _scrollToBottom();

    try {
      final response = await _groqService.sendMessage(text);

      setState(() {
        _messages.add(ChatMessage(text: response, isUser: false));
        _isLoading = false;
      });

      _scrollToBottom();
    } catch (e) {
      setState(() {
        _messages.add(
          ChatMessage(
            text: e.toString().replaceAll('Exception: ', ''),
            isUser: false,
          ),
        );
        _isLoading = false;
      });
    }
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  void dispose() {
    _textController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final languageProvider = Provider.of<LanguageProvider>(context);

    // Update service languages when language changes
    _groqService.setLanguage(languageProvider.locale.languageCode);

    return Scaffold(
      appBar: AppBar(
        title: Text(l10n.aiAssistantTitle),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Column(
        children: [
          // Quick action buttons
          Container(
            padding: const EdgeInsets.all(8),
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: [
                  _buildQuickActionChip(
                    l10n.commonDiseases,
                    () => _sendMessage(
                      languageProvider.isEnglish
                          ? 'What are the most common tomato leaf diseases?'
                          : 'সবচেয়ে সাধারণ টমেটো পাতার রোগগুলি কী কী?',
                    ),
                  ),
                  const SizedBox(width: 8),
                  _buildQuickActionChip(
                    l10n.prevention,
                    () => _sendMessage(
                      languageProvider.isEnglish
                          ? 'How can I prevent tomato plant diseases?'
                          : 'কিভাবে আমি টমেটো গাছের রোগ প্রতিরোধ করতে পারি?',
                    ),
                  ),
                  const SizedBox(width: 8),
                  _buildQuickActionChip(
                    l10n.treatment,
                    () => _sendMessage(
                      languageProvider.isEnglish
                          ? 'What are general treatment options for tomato diseases?'
                          : 'টমেটো রোগের সাধারণ চিকিৎসার বিকল্পগুলি কী কী?',
                    ),
                  ),
                ],
              ),
            ),
          ),
          const Divider(height: 1),

          // Chat messages
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length + (_isLoading ? 1 : 0),
              itemBuilder: (context, index) {
                if (index == _messages.length) {
                  return _buildLoadingIndicator();
                }

                final message = _messages[index];
                return _buildMessageBubble(message);
              },
            ),
          ),

          const Divider(height: 1),

          // Input area
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: Row(
              children: [
                // Text input
                Expanded(
                  child: TextField(
                    controller: _textController,
                    decoration: InputDecoration(
                      hintText: l10n.typeMessage,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(24),
                      ),
                      contentPadding: const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 8,
                      ),
                    ),
                    onSubmitted: _sendMessage,
                    enabled: !_isLoading,
                  ),
                ),

                const SizedBox(width: 8),

                // Send button
                IconButton(
                  onPressed: _isLoading
                      ? null
                      : () => _sendMessage(_textController.text),
                  icon: const Icon(Icons.send),
                  tooltip: l10n.send,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildQuickActionChip(String label, VoidCallback onTap) {
    return ActionChip(
      label: Text(label),
      onPressed: onTap,
      avatar: const Icon(Icons.lightbulb_outline, size: 18),
    );
  }

  Widget _buildMessageBubble(ChatMessage message) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Row(
        mainAxisAlignment: message.isUser
            ? MainAxisAlignment.end
            : MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (!message.isUser) ...[
            CircleAvatar(
              backgroundColor: Colors.green.shade700,
              child: const Icon(Icons.smart_toy, color: Colors.white, size: 20),
            ),
            const SizedBox(width: 8),
          ],

          Flexible(
            child: Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: message.isUser
                    ? Colors.blue.shade700
                    : Colors.grey.shade200,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Text(
                message.text,
                style: TextStyle(
                  color: message.isUser ? Colors.white : Colors.black87,
                  fontSize: 15,
                ),
              ),
            ),
          ),

          if (message.isUser) ...[
            const SizedBox(width: 8),
            CircleAvatar(
              backgroundColor: Colors.blue.shade700,
              child: const Icon(Icons.person, color: Colors.white, size: 20),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildLoadingIndicator() {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Row(
        children: [
          CircleAvatar(
            backgroundColor: Colors.green.shade700,
            child: const Icon(Icons.smart_toy, color: Colors.white, size: 20),
          ),
          const SizedBox(width: 8),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.grey.shade200,
              borderRadius: BorderRadius.circular(16),
            ),
            child: const Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                SizedBox(
                  width: 16,
                  height: 16,
                  child: CircularProgressIndicator(strokeWidth: 2),
                ),
                SizedBox(width: 8),
                Text('Thinking...'),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
